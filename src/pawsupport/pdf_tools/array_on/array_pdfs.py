import argparse
import os
from pathlib import Path

from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
from pypdf.papersizes import Dimensions

MARGIN = 0.12


def get_scale_factor(input_size: Dimensions, output_size: Dimensions) -> float:
    return min(
        [(output_size.width / input_size.height), (output_size.height / input_size.width)]
    ) / (1 + MARGIN)


def on_a4(
        input_file: Path,
        output_file: Path,
        output_size=PaperSize.A4,
):
    if not input_file.is_file():
        raise ValueError('Invalid input file path.')
    if not output_file.is_file() or output_file.suffix != '.pdf':
        raise ValueError('Invalid output file path.')
    reader = PdfReader(input_file)

    input_size = Dimensions(reader.pages[0].mediabox.width, reader.pages[0].mediabox.height)
    scale_factor = get_scale_factor(input_size, output_size)
    resized = Dimensions(
        int(scale_factor * input_size.width),
        int(scale_factor * input_size.height)
    )

    left_translation, right_translation = get_translations(resized, output_size)

    writer = PdfWriter()

    for i in range(0, len(reader.pages), 2):
        # width and height are swapped for landscape
        d_page = writer.add_blank_page(output_size.height, output_size.width)
        for j in range(2):
            if i + j < len(reader.pages):
                page_num = i + j
                translate = left_translation if j == 0 else right_translation  # zero-indexed so swap left right
                page = reader.pages[page_num]
                page.scale_by(scale_factor)
                d_page.merge_transformed_page(page, translate)

    with open(output_file, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)


def get_translations(in_size: Dimensions, out_size: Dimensions) -> tuple[
    Transformation, Transformation]:
    x_left, x_right, y = get_translation_dims(in_size, out_size)
    return (Transformation().translate(x_left, y),
            Transformation().translate(x_right, y))


def get_translation_dims(in_size: Dimensions, out_size: Dimensions) -> tuple[float, float, float]:
    translate_x_left = (out_size.height / 2 - in_size.width) / 2
    translate_x_right = (out_size.height / 2 - in_size.width) / 2 + out_size.height / 2
    translate_y = (out_size.width - in_size.height) / 2

    return translate_x_left, translate_x_right, translate_y


def main():
    parser = argparse.ArgumentParser(description='Scale and arrange PDF pages on A4 sheets.')
    parser.add_argument('input', help='Path to the input PDF file or dir with PDF files')
    parser.add_argument(
        '-o',
        '--out_dir',
        help='Path to the output dir, optional - defaults to cwd/output'
    )
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print the output PDF after processing'
    )

    args = parser.parse_args()
    print(args)
    inpath = Path(args.input)
    if inpath.is_file():
        input_files = [Path(args.input)]
    elif inpath.is_dir():
        input_files = list(inpath.glob('*.pdf'))
    else:
        raise ValueError('Invalid input path - must be a PDF file or a directory.')

    output_dir = args.out_dir or Path.cwd() / 'output'
    convert_many(input_files, output_dir, print_files=args.print)


def convert_many(input_files: list[Path], output_dir: Path, *, print_files=False):
    output_dir.mkdir(exist_ok=True)
    for file in input_files:
        output_file = output_dir / f'{file.stem}_on_a4.pdf'
        print(f'Processing {file.name}...')
        on_a4(file, output_file)
        print(f'Output file: {output_file}')
        if print_files:
            os.startfile(output_file, 'print')


if __name__ == '__main__':
    main()
