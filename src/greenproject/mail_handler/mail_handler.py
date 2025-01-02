import emails

class MailHandler:
    def __init__(self, smtp_host, smtp_user, smtp_password):
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
    
    def send_email(self, subject, body, to_email):
        """
        Send an email with the provided subject and body.
        :param subject: Subject of the email.
        :param body: Body content of the email.
        :param to_email: Recipient email address.
        """
        try:
            # Create the email message
            msg = emails.Message(
                subject=subject, 
                mail_from=self.smtp_user, 
                text=body
            ).send(
                to=to_email,
                smtp={
                    "host": self.smtp_host,
                    "tls": True,
                    "user": self.smtp_user,
                    "password": self.smtp_password,
                },
            )
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")