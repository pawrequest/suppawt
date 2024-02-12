import argparse
import os
from pathlib import Path

from loguru import logger
from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
from pypdf.papersizes import Dimensions

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
    parser = argparse.ArgumentParser(description='Scale and arrange PDF pages on A4 sheets.')
    parser.add_argument('-o', '--input_dir', help='Path to the input directory, defaults to script dir')
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print output PDF/s after processing'
    )
    args = parser.parse_args()

    script_dir = Path(args.input_dir) or Path(__file__).parent
    output_dir = script_dir / 'output'

    convert_all(script_dir, output_dir, print_files=args.print)


def convert_all(input_dir, output_dir, print_files=False):
    output_dir.mkdir(exist_ok=True)
    for file in input_dir.glob('*.pdf'):
        output_file = output_dir / f'{file.stem}_on_a4.pdf'
        on_a4(file, output_file)
        if print_files:
            os.startfile(output_file, 'print')


if __name__ == '__main__':
    main()
