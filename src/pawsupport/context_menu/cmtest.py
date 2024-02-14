from context_menu import menus


def foo1(filenames, params):
    print(filenames)
    input()


MENU_NAME = 'Example Fast Command 1'


def remove_menu():
    menus.removeMenu(MENU_NAME, 'FILES')


if __name__ == '__main__':
    # fc = menus.FastCommand(MENU_NAME, type='FILES', python=foo1)
    # fc.compile()
    remove_menu()


def go(input_files):
    output_dir = Path.cwd() / 'pdf_array'
    convert_many(input_files, output_dir, print_files=True)