import argparse
import os
from pathlib import Path

from ..array_pdfs import on_a4


def main():
    parser = argparse.ArgumentParser(description='Scale and arrange PDF pages on A4 sheets.')
    parser.add_argument(
        '-o',
        '--input_dir',
        help='Path to the input directory, defaults to script dir'
    )
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print output PDF/s after processing'
    )
    args = parser.parse_args()

    script_dir = Path(args.input_dir) or Path(__file__).parent
    output_dir = script_dir / 'output'

    convert_all(script_dir, output_dir, print_files=args.print)


def convert_all(input_dir: Path, output_dir: Path, print_files=False):
    output_dir.mkdir(exist_ok=True)
    for file in input_dir.glob('*.pdf'):
        output_file = output_dir / f'{file.stem}_on_a4.pdf'
        on_a4(file, output_file)
        if print_files:
            os.startfile(output_file, 'print')


if __name__ == '__main__':
    main()
