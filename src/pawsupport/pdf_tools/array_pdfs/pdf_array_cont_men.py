import argparse
import os
import sys
from pathlib import Path

from context_menu import menus
from loguru import logger

from pawsupport.src.pawsupport.pdf_tools.array_pdfs.array import convert_many

MENU_NAME = 'Array and Print PDF'


def do_menu(input_files, extra):
    try:
        logger.disable(__name__)
        # output_dir = Path(r'R:\Parcelforce Labels\arrayed')
        output_dir = Path.cwd() / 'pdf_array'
        print(f'{output_dir=}')
        input_paths = [Path(_) for _ in input_files]
        ans = input('\nEnter [P/p] to print, [O/o] to open, other to exit\n')
        prnt = ans.lower() == 'p'
        openit = ans.lower() == 'o'

        convert_many(input_files=input_paths, output_dir=output_dir, print_files=prnt)
        if openit:
            opener = input_paths[0]
            output_file = output_dir / f'{opener.stem}_on_a4.pdf'
            os.startfile(output_file)

    except Exception as e:
        print(e)
        input('Press enter to continue')
    else:
        sys.exit(0)


def remove_menu():
    menus.removeMenu(MENU_NAME, 'FILES')


def add_menu():
    fc = menus.FastCommand(MENU_NAME, type='FILES', python=do_menu)
    fc.compile()


def main():
    parser = argparse.ArgumentParser(description='Install or remove the context menu for PDF files.')
    parser.add_argument('in_or_rm', help='Install or remove the context menu')

    args = parser.parse_args()
    if args.in_or_rm == 'install':
        add_menu()
    elif args.in_or_rm == 'remove':
        remove_menu()
    else:
        raise ValueError('Invalid argument - must be "install" or "remove"')


if __name__ == '__main__':
    main()
