import platform
import subprocess
import webbrowser
from pathlib import Path
from typing import Any

from pawsupport.office_ps.doc_handler import DocHandler


class LibreHandler(DocHandler):
    def display_doc(self, doc_path: Path) -> tuple[Any, Any]:
        """
        Display a document

        :param doc_path: path to document
        :return: process, None
        """
        try:
            process = subprocess.Popen(
                ['soffice', str(doc_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as e:
            raise e
        return process, None

    def to_pdf(self, doc_file: Path) -> Path:
        """
        Convert a document to pdf

        :param doc_file: path to document
        :return: path to pdf
        """
        try:
            subprocess.run(
                f'soffice --headless --convert-to pdf '
                f'{str(doc_file)} --outdir {str(doc_file.parent)}'
            )
            outfile = doc_file.with_suffix('.pdf')
            print(f'Converted {outfile}')
            return outfile
        except FileNotFoundError:
            print('Is LibreOffice installed?')
            raise FileNotFoundError('LibreOffice not installed')


def get_libre_platform() -> tuple[str, str, str]:
    """
    Get the platform for libreoffice

    :return: platform tuple (os, arch, file)
    """
    system = platform.system()
    architecture = platform.architecture()[0]

    if system == 'Windows':
        if '64' in architecture:
            return 'win', 'x86_64', 'Win_x86-64.msi'
        else:
            return 'win', 'x86', 'Win_x86.msi'
    elif system == 'Darwin':  # macOS
        return 'mac', 'aarch64', 'MacOS_aarch64.dmg'
    elif system == 'Linux':
        # todo check debian vs other
        if '64' in architecture:
            return 'deb', 'x86_64', 'Linux_x86-64_deb.tar.gz'
        else:
            return 'deb', 'x86', 'Linux_x86_deb.tar.gz'
    else:
        raise OSError(f'Unsupported system: {system}')


def go_install_libre(version='7.6.2') -> bool:
    """
    Open the libreoffice download page

    :param version: version to download
    :return: True
    """
    plat = get_libre_platform()
    dl = f'https://www.libreoffice.org/donate/dl/{plat[0]}-{plat[1]}/{version}/en-US/LibreOffice_{version}_{plat[2]}'
    webbrowser.open(dl)
    return True


def direct_libre_dl() -> str:
    """
    Get the direct download link for libreoffice

    :return: direct download link
    """
    libre_platform = get_libre_platform()
    libre_version = '7.6.2'
    dl = f'https://download.documentfoundation.org/libreoffice/stable/{libre_version}/{libre_platform[0]}/{libre_platform[1]}/LibreOffice_{libre_version}_{libre_platform[2]}'
    return dl
