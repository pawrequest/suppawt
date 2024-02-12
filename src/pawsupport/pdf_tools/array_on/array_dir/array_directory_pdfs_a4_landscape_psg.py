import os
import sys
from pathlib import Path

from loguru import logger
from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
from pypdf.papersizes import Dimensions
import PySimpleGUI as sg

MARGIN = 0.12


def get_scale_factor(input_size: Dimensions, output_size: Dimensions) -> float:
    return min(
        [(output_size.width / input_size.height), (output_size.height / input_size.width)]
    ) / (1 + MARGIN)


def on_a4(
        input_path: Path,
        output_path: Path,
        output_size=PaperSize.A4,
):
    if not input_path.is_file():
        logger.error(f'File not found: {input_path}')
        return
    if not input_path.suffix == '.pdf':
        logger.error(f'File is not a PDF: {input_path}')
        return
    reader = PdfReader(input_path)
    input_size = Dimensions(reader.pages[0].mediabox.width, reader.pages[0].mediabox.height)

    scale_factor = get_scale_factor(input_size, output_size)
    resized = Dimensions(
        int(scale_factor * input_size.width),
        int(scale_factor * input_size.height)
    )
    landscape_dims = Dimensions(output_size.height, output_size.width)

    translate_x_left, translate_x_right, translate_y = get_translations(output_size, resized)

    writer = PdfWriter()

    for i in range(0, len(reader.pages), 2):
        page = writer.add_blank_page(*landscape_dims)

        left = reader.pages[i]
        left.scale_by(scale_factor)
        translation = Transformation().translate(translate_x_left, translate_y)
        # if left.mediabox.width > left.mediabox.height:
        #     logger.info(f'Page {i} is landscape - rotating 90 degrees.')
        #     left.rotate(90)
        page.merge_transformed_page(left, translation)

        if i + 1 < len(reader.pages):
            right = reader.pages[i + 1]
            if right.mediabox.width > right.mediabox.height:
                logger.info(f'Page {i + 1} is landscape - rotating 90 degrees.')
                right.rotate(90)
            right.scale_by(scale_factor)
            translation = Transformation().translate(translate_x_right, translate_y)
            page.merge_transformed_page(right, translation)

    with open(output_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)
    # os.startfile(output_pdf_path, 'print')


def get_translations(output_size: Dimensions, resized: Dimensions) -> tuple[float, float, float]:
    translate_x_left = (output_size.height / 2 - resized.width) / 2
    translate_x_right = (output_size.height / 2 - resized.width) / 2 + output_size.height / 2
    translate_y = (output_size.width - resized.height) / 2

    return translate_x_left, translate_x_right, translate_y


def main():
    answer = sg.popup_yes_no(
        'Convert All?',
        'Convert all files in the current directory to A4? (No to select a file)'
    )
    script_dir = Path(__file__).parent
    output_dir = script_dir / 'output'
    if answer == 'Yes':
        convert_all(script_dir, output_dir)
    else:
        input_file, prnt = get_file_window()

        if input_file:
            output_file = output_dir / input_file.with_name(f'{input_file.stem}_on_a4.pdf')
            on_a4(input_file, output_file)
            if prnt:
                os.startfile(str(output_file), 'print')


def get_file_window() -> tuple[Path, bool]:
    """Get a file from the user.
    :return: the file path and whether to print after conversion
    """
    layout = [

        [sg.Text('Select a PDF ')],
        [sg.InputText(), sg.FileBrowse()],
        [sg.Checkbox('Print after conversion', default=True, key='--PRINT--')],
        [sg.Button('Ok'), sg.Button('Cancel')],
    ]

    window = sg.Window('Select a PDF file', layout)
    while True:
        event, values = window.read()
        prnt = values['--PRINT--']
        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            sys.exit('Aborted')
        if event == 'Ok':
            window.close()
            return Path(values[0]), prnt


def convert_all(input_dir, output_dir):
    output_dir.mkdir(exist_ok=True)
    for file in input_dir.glob('*.pdf'):
        on_a4(file, output_dir / f'{file.name}_on_a4.pdf')


if __name__ == '__main__':
    main()
