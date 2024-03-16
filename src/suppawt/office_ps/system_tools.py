import asyncio
import os
import shutil
import winreg as reg
from pathlib import Path

"""
functions for system tools
"""


def print_file(file_path: Path) -> bool:
    """
    Print a file

    :param file_path: path to file
    :return: True if successful, False otherwise
    """
    try:
        os.startfile(str(file_path), 'print')
        return True
    except Exception as e:
        print(f'Failed to print: {e}')
        return False


async def wait_for_process(process) -> None:
    """
    Wait for a process to finish

    :param process: process to wait for
    :return: None
    """
    while True:
        res = process.poll()
        if res is not None:
            break
        await asyncio.sleep(3)
    print('Process has finished.')


def check_registry(reg_path: str) -> bool:
    """
    Check if a registry path exists

    :param reg_path: registry path to check
    :return: True if registry path exists, False otherwise
    """
    try:
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path)
        reg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def check_word() -> bool:
    """
    Check if Microsoft Word is installed

    :return: True if Microsoft Word is installed"""
    return check_registry(
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WINWORD.EXE'
    )


def check_excel() -> bool:
    """
    Check if Microsoft Excel is installed

    :return: True if Microsoft Excel is installed"""
    return check_registry(
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\EXCEL.EXE'
    )


def check_lib2() -> bool:
    """
    Check if LibreOffice is installed

    :return: True if LibreOffice is installed"""
    return check_registry(r'SOFTWARE\LibreOffice')


def check_libre() -> bool:
    """
    Check if LibreOffice is installed

    :return: True if LibreOffice is installed"""
    return shutil.which(r'soffice.exe') is not None


def check_outlook() -> bool:
    """
    Check if Microsoft Outlook is installed

    :return: True if Microsoft Outlook is installed"""
    return check_registry(
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\OUTLOOK.EXE'
    )
