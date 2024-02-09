from PyPDF2 import PdfReader, PdfWriter, Transformation
from PyPDF2.papersizes import PaperSize


def center_a6_on_a5gpt(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    a5_width, a5_height = PaperSize.A5
    a6_width, a6_height = PaperSize.A6

    x_margin = (a5_width - a6_width) / 2
    y_margin = (a5_height - a6_height) / 2

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        # Create a new blank A5 page
        new_page = writer.add_blank_page(width=a5_width, height=a5_height)
        # Merge the A6 page content onto the new A5 page, centered
        new_page.merge_scaled_translated_page(page, 1, x_margin, y_margin)

    with open(output_pdf_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)


a5_width, a5_height = PaperSize.A5
a6_width, a6_height = PaperSize.A6

x_margin = (a5_width - a6_width) / 2
y_margin = (a5_height - a6_height) / 2


def on_a4(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        new_page = writer.add_blank_page(width=PaperSize.A4[0], height=PaperSize.A4[1])

        # page.rotate(90)
        scale_content = Transformation().scale(sx=0.5, sy=0.5)
        page.add_transformation(scale_content)
        translation = [x_margin, 0]
        page.add_transformation(Transformation().translate(*translation))

        new_page.merge_page(page)

        # writer.add_page(new_page)
        writer.add_page(page)


    with open(output_pdf_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)


def center_a6_on_a5(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        # page.rotate(90)
        # page.scale_by(1.5)
        #
        # center_content = Transformation().translate(tx=x_margin, ty=y_margin)
        # page.add_transformation(center_content)
        #
        # writer.add_page(page)

        # scale canvas
        page.scale_by(0.5)

        # # scale content
        op = Transformation().scale(sx=0.7, sy=0.7)
        page.add_transformation(op)

        new_page = writer.add_blank_page(width=a5_width, height=a5_height)
        new_page.merge_page(page)
        #
        writer.add_page(new_page)

    with open(output_pdf_path, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)


def main():
    # center_a6_on_a5('label.pdf', 'centered_on_a5.pdf')
    on_a4('label.pdf', 'on_a4.pdf')


if __name__ == '__main__':
    main()
