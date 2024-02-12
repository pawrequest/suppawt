import argparse
import os

from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
from pypdf.papersizes import Dimensions

MARGIN = 0.12


def get_scale_factor(input_size: Dimensions, output_size: Dimensions) -> float:
    return min(
        [(output_size.width / input_size.height), (output_size.height / input_size.width)]
    ) / (1 + MARGIN)


def on_a4(
        input_pdf_path,
        output_pdf_path,
        output_size=PaperSize.A4,
):
    reader = PdfReader(input_pdf_path)

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
            right.scale_by(scale_factor)
            translation = Transformation().translate(translate_x_right, translate_y)
            page.merge_transformed_page(right, translation)

    with open(output_pdf_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)
    # os.startfile(output_pdf_path, 'print')


def get_translations(output_size: Dimensions, resized: Dimensions) -> tuple[float, float, float]:
    translate_x_left = (output_size.height / 2 - resized.width) / 2
    translate_x_right = (output_size.height / 2 - resized.width) / 2 + output_size.height / 2
    translate_y = (output_size.width - resized.height) / 2

    return translate_x_left, translate_x_right, translate_y


def main():
    parser = argparse.ArgumentParser(description='Scale and arrange PDF pages on A4 sheets.')
    parser.add_argument('input', help='Path to the input PDF file')
    parser.add_argument('-o', '--output', help='Path to the output PDF file, optional')
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print the output PDF after processing'
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output if args.output else input_path.rsplit('.', 1)[0] + '_on_a4.pdf'
    on_a4(input_path, output_path)
    if args.print:
        os.startfile(str(output_path), 'print')


if __name__ == '__main__':
    main()
