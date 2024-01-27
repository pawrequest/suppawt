class OutlookHandler(EmailHandler):
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
