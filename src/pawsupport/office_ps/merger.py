"""
functions for merging docx templates
"""
from pathlib import Path
from typing import Tuple

import PySimpleGUI as sg
from docxtpl import DocxTemplate


def get_template_and_path(tmplt, temp_file, context=None) -> Tuple[DocxTemplate, Path]:
    """
    Get a docx template and save it to a temporary file

    :param tmplt: path to template
    :param temp_file: path to temporary file
    :param context: context to render template with
    :return: tuple of template and temporary file
    """
    context = context or dict()
    template = DocxTemplate(tmplt)
    template.render(context)

    while True:
        try:
            template.save(temp_file)
            return template, temp_file
        except Exception as e:
            if sg.popup_ok_cancel('Close the template file and try again') == 'OK':
                continue
            else:
                raise e


def try_again() -> str:
    """
    Popup to try again or cancel

    :return: 'OK' or 'Cancel'
    """
    return sg.popup_ok_cancel('Close the template file and try again')


def get_template(tmplt, temp_file, context=None) -> DocxTemplate:
    """
    Get a docx template and save it to a temporary file

    :param tmplt: path to template
    :param temp_file: path to temporary file
    :param context: context to render template with
    :return: template
    """
    template = DocxTemplate(tmplt)

    while True:
        try:
            template.render(context)
            template.save(temp_file)
            return template
        except Exception as e:
            ans = try_again()
            if ans == 'OK':
                continue
            raise e


def templt_to_pdf(tmplt, context, doc_handler, temp_file) -> Path:
    """
    Render a docx template to a pdf

    :param tmplt: path to template
    :param context: context to render template with
    :param doc_handler: doc handler to use
    :param temp_file: path to temporary file
    :return: path to pdf
    """
    try:
        template = DocxTemplate(tmplt)
        template.render(context)
        template.save(temp_file)
        pdf_file = doc_handler.to_pdf(temp_file)
    except Exception:
        ...
    else:
        return pdf_file
