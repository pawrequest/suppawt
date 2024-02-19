import argparse

from .pdf_array_cont_men import add_menu, remove_menu


def main():
    parser = argparse.ArgumentParser(
        description='Install or remove the context menu for PDF files.'
    )
    parser.add_argument(
        'action',
        choices=['install', 'remove'],
        help='Action to perform: install or remove the context menu'
    )

    args = parser.parse_args()

    if args.action == 'install':
        add_menu()
    elif args.action == 'remove':
        remove_menu()


if __name__ == '__main__':
    main()
