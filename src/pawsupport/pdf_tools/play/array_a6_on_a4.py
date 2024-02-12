from pypdf import PaperSize, PdfReader, PdfWriter


def on_a4(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for i in range(0, len(reader.pages), 2):
        destpage = writer.add_blank_page(width=PaperSize.A4.height, height=PaperSize.A4.width)
        left = reader.pages[i]
        translation_y = (PaperSize.A4.width - left.mediabox.height) / 2
        translation_x = (PaperSize.A4.height / 2 - left.mediabox.width) / 2
        destpage.merge_translated_page(left, translation_x, translation_y)

        if i + 1 < len(reader.pages):
            right = reader.pages[i + 1]
            translation_y = (PaperSize.A4.width - right.mediabox.height) / 2
            translation_x = (PaperSize.A4.height / 2 - right.mediabox.width) / 2
            destpage.merge_translated_page(right, translation_x, translation_y)

            # transform = Transformation().translate(
            #     PaperSize.A4.height / 2 + translation_x,
            #     translation_y
            #     )
            # destpage.merge_transformed_page(right, transform)

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
