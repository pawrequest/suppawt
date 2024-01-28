import webbrowser

from pawsupport.office_ps.email_handler import EmailHandler, Email


class GmailHandler(EmailHandler):
    def send_email(self, email: Email) -> None:
        compose_link = gmail_compose_link(email)
        webbrowser.open(compose_link)
        print(
            'Opened Gmail compose window, no attachment possible, '
            'please attach manually, implement better solution i.e. gmail oauth'
        )


def gmail_compose_link(email: Email) -> str:
    to_encoded = email.to_address.replace('@', '%40')
    subject_encoded = email.subject.replace(' ', '%20')
    body_encoded = email.body.replace(' ', '%20')
    compose_link = (
        f'https://mail.google.com/mail/u/0/?view=cm&fs=1&to='
        f'{to_encoded}&su={subject_encoded}&body={body_encoded}'
    )
    return compose_link
