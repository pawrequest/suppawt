from src.office_tools.doc_handler import DocHandler
from src.office_tools.email_handler import EmailHandler, Email, EmailError


class WordHandler(DocHandler):
    # todo use library
    def display_doc(self, doc_path: Path) -> Tuple[Any, Any]:
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
            convert_word(doc_file, output_path=doc_file.parent)
            outfile = doc_file.with_suffix('.pdf')
            print(f'Converted {outfile}')
            return outfile
        except Exception as e:
            raise e


class OutlookSender(EmailHandler):
    def send_email(self, email: Email):
        try:
            outlook = Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = email.to_address
            mail.Subject = email.subject
            mail.Body = email.body
            if email.attachment_path:
                mail.Attachments.Add(str(email.attachment_path))
                print('Added attachment')
            print('Sending email [disabled - uncomment to enable]')
            # mail.Display()
            # mail = None
            # mail.Send()
        except com_error as e:
            msg = f'Outlook not installed - {e.args[0]}'
            print(msg)
            raise EmailError(msg)
        except Exception as e:
            msg = f'Failed to send email with error: {e.args[0]}'
            print(msg)
            raise EmailError(msg)
