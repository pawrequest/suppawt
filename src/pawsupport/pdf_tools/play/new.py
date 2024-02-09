from PyPDF2 import PdfReader, PdfWriter, Transformation
from PyPDF2.papersizes import PaperSize


def on_a4(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for i in range(0, len(reader.pages), 2):
        # Create a new A4 page
        new_page = writer.add_blank_page(width=PaperSize.A4[1], height=PaperSize.A4[0])

        if i < len(reader.pages):
            left = reader.pages[i]
            left.rotate(90)
            left.scale(4, 4)
            left.artbox.scale(.5, .5)
            new_page.merge_page(left)

        # if i + 1 < len(reader.pages):
        #     right = reader.pages[i + 1]
        #     transform = Transformation().translate(PaperSize.A4[1] / 2, 0)
        #     right.add_transformation(transform)
        #     new_page.merge_page(right)

    # Write the output PDF
    with open(output_pdf_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)


def main():
    on_a4('label.pdf', 'on_a4.pdf')


if __name__ == '__main__':
    main()
