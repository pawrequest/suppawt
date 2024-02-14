from pathlib import Path

from context_menu import menus

from pawsupport.src.pawsupport.pdf_tools.array_pdfs.array import convert_many


def foo1(filenames, params):
    print(filenames)
    input()


MENU_NAME = 'Array and Print PDF'


def remove_menu():
    menus.removeMenu(MENU_NAME, 'FILES')


def go(input_files):
    output_dir = Path.cwd() / 'pdf_array'
    convert_many(input_files, output_dir, print_files=True)

#
# fc = menus.FastCommand(MENU_NAME, type='FILES', python=go)
# fc.compile()

remove_menu()
