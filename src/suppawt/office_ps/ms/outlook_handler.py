import pythoncom
from loguru import logger
from win32com.client import Dispatch

from suppawt.office_ps.email_handler import (
    Email,
    EmailError,
    EmailHandler,
)


def emailer(email: Email, html: bool = False):
    """
    Send email via Outlook

    :param email: Email object
    :param html: bool indicating if email is HTML
    :return: None
    """
    try:
        pythoncom.CoInitialize()
        outlook = Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = email.to_address
        mail.Subject = email.subject
        if html:
            mail.HTMLBody = email.body
        else:
            mail.Body = email.body
        for att_path in email.attachment_paths:
            mail.Attachments.Add(str(att_path))
            print('Added attachment')
        mail.Display()
    except Exception as e:
        logger.exception(f'Failed to send email with error: {e}')
        raise EmailError(f'{e.args[0]}')
    finally:
        pythoncom.CoUninitialize()


class OutlookHandler(EmailHandler):
    """
    Email handler for Outlook
    """

    def create_open_email(self, email: Email):
        """
        Send email via Outlook

        :param email: Email object
        :return: None
        """
        try:
            pythoncom.CoInitialize()

            outlook = Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = email.to_address
            mail.Subject = email.subject
            mail.Body = email.body
            for att_path in email.attachment_paths:
                mail.Attachments.Add(str(att_path))
                print('Added attachment')
            mail.Display()
        except Exception as e:
            logger.exception(f'Failed to send email with error: {e}')
            raise EmailError(f'{e.args[0]}')
        finally:
            pythoncom.CoUninitialize()
