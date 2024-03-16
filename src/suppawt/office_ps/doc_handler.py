import platform
import subprocess
import webbrowser
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple

from comtypes.client import CreateObject  # type: ignore
from docx2pdf import convert as convert_word  # type: ignore


class DocHandler(ABC):
    """
    Abstract class for handling documents
    """
    @abstractmethod
    def display_doc(self, doc_path: Path) -> Tuple[Any, Any]:
        """
        Display a document

        :param doc_path: Path to document
        :return: Process and document
        """
        raise NotImplementedError

    @abstractmethod
    def to_pdf(self, doc_file: Path) -> Path:
        """
        Convert document to PDF

        :param doc_file: Path to document
        :return: Path to PDF
        """
        raise NotImplementedError


