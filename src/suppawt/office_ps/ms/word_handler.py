from pathlib import Path
from typing import Tuple, Any

from comtypes.client import CreateObject
from docx2pdf import convert
from suppawt.office_ps.doc_handler import DocHandler


class WordHandler(DocHandler):
    # todo use library
    def display_doc(self, doc_path: Path) -> tuple[Any, Any]:
        try:
            word = CreateObject('Word.Application')
            word.Visible = True
            word_doc = word.Documents.Open(str(doc_path))
            return word, word_doc
        except OSError as e:
            print(f'Is Word installed? Failed to open {doc_path} with error: {e}')
            raise e
        except Exception as e:
            raise e

    def to_pdf(self, doc_file: Path) -> Path:
        try:
            convert(doc_file, output_path=doc_file.parent)
            outfile = doc_file.with_suffix('.pdf')
            print(f'Converted {outfile}')
            return outfile
        except Exception as e:
            raise e
