import webbrowser

from suppawt.office_ps.email_handler import EmailHandler, Email


class GmailHandler(EmailHandler):
    """
    GmailHandler opens a Gmail compose window with the email details.
    """
    def send_email(self, email: Email) -> None:
        """"
        Opens a Gmail compose window with the email details.

        :param email: Email object with details to send.
        """
        compose_link = gmail_compose_link(email)
        webbrowser.open(compose_link)
        print(
            'Opened Gmail compose window, no attachment possible, '
            'please attach manually, implement better solution i.e. gmail oauth'
        )


def gmail_compose_link(email: Email) -> str:
    """
    Returns a Gmail compose link with the email details.

    :param email: Email object with details to send.
    :return: Gmail compose link with the email details.
    """
    to_encoded = email.to_address.replace('@', '%40')
    subject_encoded = email.subject.replace(' ', '%20')
    body_encoded = email.body.replace(' ', '%20')
    compose_link = (
        f'https://mail.google.com/mail/u/0/?view=cm&fs=1&to='
        f'{to_encoded}&su={subject_encoded}&body={body_encoded}'
    )
    return compose_link
