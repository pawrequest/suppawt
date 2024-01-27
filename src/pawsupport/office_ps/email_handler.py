import webbrowser
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from win32com.client import Dispatch
from win32com.universal import com_error


class EmailHandler(ABC):
    @abstractmethod
    def send_email(self, email: 'Email') -> None:
        ...


@dataclass
class Email:
    to_address: str
    subject: str
    body: str
    attachment_path: Path or None = None

    def send(self, sender: EmailHandler) -> None:
        sender.send_email(self)


class EmailError(Exception):
    ...


