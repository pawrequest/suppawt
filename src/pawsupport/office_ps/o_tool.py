import itertools

from .doc_handler import DocHandler
from .foss.gmail_handler import GmailHandler
from .foss.libre_handler import LibreHandler
from .ms.outlook_handler import OutlookHandler
from .ms.word_handler import WordHandler
from .system_tools import (check_excel, check_lib2, check_libre, check_outlook, check_word)
from .email_handler import EmailHandler


class OfficeTools:
    """
    Class for handling office tools

    :param doc: doc handler
    :param email: email handler
    """

    def __init__(self, doc: DocHandler, email: EmailHandler):
        self.doc: DocHandler = doc
        self.email: EmailHandler = email

    @classmethod
    def microsoft(cls) -> 'OfficeTools':
        """
        Get office tools for Microsoft Office
        :return: OfficeTools instance"""
        try:
            return cls(WordHandler(), OutlookHandler())
        except OSError:
            raise OSError('Microsoft Office tools are not installed')

    @classmethod
    def libre(cls) -> 'OfficeTools':
        """
        Get office tools for LibreOffice
        :return: OfficeTools instance"""

        try:
            return cls(LibreHandler(), GmailHandler())
        except OSError:
            raise OSError('LibreOffice tools are not installed')

    @classmethod
    def auto_select(cls) -> 'OfficeTools':
        """
        Automatically select office tools - Microsoft if installed, Libre otherwise
        :return: OfficeTools instance"""

        if not tools_available():
            raise OSError('Neither Microsoft nor LibreOffice tools are installed')

        doc_handler = WordHandler if check_word() else LibreHandler
        email_handler = OutlookHandler if check_outlook() else GmailHandler

        return cls(doc_handler(), email_handler())


def tools_available() -> bool:
    """
    Check if either [Microsoft or LibreOffice] tools for docs and sheets are installed

    :return: True if either Microsoft or LibreOffice tools for docs and sheets are installed, False otherwise
    """
    libre = check_libre()
    word = check_word()
    excel = check_excel()
    return all([(word or libre), (excel or libre)])


def get_installed_combinations():
    """
    Get all installed combinations of doc and email handlers

    :return: list of OfficeTools instances
    """
    doc_handlers = []
    email_handlers = []

    if check_word():
        doc_handlers.append(WordHandler)
    if check_lib2():
        doc_handlers.append(LibreHandler)

    if check_outlook():
        email_handlers.append(OutlookHandler)

    email_handlers.append(GmailHandler)

    for doc_handler, email_handler in itertools.product(doc_handlers, email_handlers):
        yield OfficeTools(doc_handler(), email_handler())
