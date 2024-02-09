
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.papersizes import PaperSize

a5_width, a5_height = PaperSize.A5
a6_width, a6_height = PaperSize.A6
x_margin = (a5_width - a6_width) / 2
y_margin = (a5_height - a6_height) / 2


def on_a4(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        # page.scale(0.5, 0.5)
        # page.cropbox.scale(2, 2)

        new_page = writer.add_blank_page(width=PaperSize.A4[1], height=PaperSize.A4[0])
        # writer.add_page(new_page)

        new_page.merge_page(page)

        # translation = [x_margin, 0]

        # page.rotate(90)
        # page.add_transformation(Transformation().translate(*translation))
        # writer.add_page(page)

    with open(output_pdf_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)

    # os.startfile(str(out_pdf_file), 'print')


def main():
    on_a4('label.pdf', 'on_a4.pdf')


if __name__ == '__main__':
    main()
