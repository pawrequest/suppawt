# import copy
#
# from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
#
# BUMP_LEFT = 30
# INPUT_SIZE = PaperSize.A6
# OUTPUT_SIZE = PaperSize.A4
# # SCALE_FACTOR = (PaperSize.A5.width / PaperSize.A6.width) * 0.8
# TRANSLATE_X_LEFT = (OUTPUT_SIZE.height / 2 - INPUT_SIZE.width) / 2
# TRANSLATE_X_RIGHT = (OUTPUT_SIZE.height / 2 - INPUT_SIZE.width) / 2 + OUTPUT_SIZE.height / 2
# translate_y = (OUTPUT_SIZE.width - INPUT_SIZE.height) / 2
#
# SCALE_FACTOR = 1.2
# def on_a4(input_pdf_path, output_pdf_path):
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()
#
#     for i in range(0, len(reader.pages), 2):
#         destpage = writer.add_blank_page(width=PaperSize.A4.height, height=PaperSize.A4.width)
#         left = copy.copy(reader.pages[i])
#
#         left.scale_by(SCALE_FACTOR)
#
#         translation = Transformation().translate(
#             (PaperSize.A4.height / 2 - left.cropbox.width) / 2,
#             # 0,
#             (PaperSize.A4.width - left.cropbox.height) / 2
#         )
#
#         destpage.merge_transformed_page(left, translation)
#
#
#         # if i + 1 < len(reader.pages):
#         #     right = reader.pages[i + 1]
#         if True:
#             right = copy.copy(reader.pages[i])
#
#             right.scale_by(SCALE_FACTOR)
#
#             translation = Transformation().translate(
#                 ((PaperSize.A4.height / 2 - left.cropbox.width) / 2) + PaperSize.A4.height / 2,
#
#                 (PaperSize.A4.width - left.cropbox.height) / 2
#
#             )
#             # right.add_transformation(translation)
#
#             destpage.merge_transformed_page(right, translation)
#
#             # translation_y = (PaperSize.A4.width - right.mediabox.height) / 2
#             # translation_x = (PaperSize.A4.height / 2 - right.mediabox.width) / 2
#             # destpage.merge_translated_page(right, translation_x, translation_y)
#
#     with open(output_pdf_path, 'wb') as out_pdf_file:
#         writer.write(out_pdf_file)
#     # os.startfile(output_pdf_path, 'print')
#
#
# def main():
#     on_a4('label.pdf', 'on_a4.pdf')
#
#
# if __name__ == '__main__':
#     main()
