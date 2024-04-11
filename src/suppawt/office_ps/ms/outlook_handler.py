import pythoncom
from loguru import logger
from win32com.client import Dispatch
from win32com.universal import com_error

from suppawt.office_ps.email_handler import EmailHandler, Email, EmailError


class OutlookHandler(EmailHandler):
    """
    Email handler for Outlook
    """
    def send_email(self, email: Email):
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
            if email.attachment_path:
                mail.Attachments.Add(str(email.attachment_path))
                print('Added attachment')
            # print('Sending email [disabled - uncomment to enable]')
            mail.Display()
            # mail = None
            # mail.Send()
        except Exception as e:
            logger.exception(f'Failed to send email with error: {e}')
            raise EmailError(f'{e.args[0]}')
        finally:
            pythoncom.CoUninitialize()

# def send_email(email):
#     try:
#         # Initialize the COM library for the current thread
#         pythoncom.CoInitialize()
#
#         outlook = Dispatch('outlook.application')
#         mail = outlook.CreateItem(0)
#         mail.To = email.to_address
#         mail.Subject = email.subject
#         mail.Body = email.body
#         if email.attachment_path:
#             mail.Attachments.Add(str(email.attachment_path))
#         mail.Send()
#
#     except Exception as e:
#         raise EmailError(f"Outlook not installed - {e.args[0]}")
#     finally:
#         # Uninitialize the COM library for the current thread
#         pythoncom.CoUninitialize()