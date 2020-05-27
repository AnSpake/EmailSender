#!/usr/bin/env python3

from smtpd import SMTPServer
import smtplib, ssl

class EmailServer():
    """
        Secure SMTP Server
    """

    def __init__(self, hostname, port, enable_ssl : bool =False):
        self.hostname = hostname
        self.port = port

        if enable_ssl:
            self.context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(hostname, port, context=self.context)

    def sendmail(self, email_obj):
        self.server.sendmail(email_obj['Sender']
                            , email_obj['To']
                            , email_obj.as_string())

    def __enter__(self):
        return self

    def quit(self):
        self.server.quit()

    def __exit__(self, exec_type, exec_value, tb):
        self.quit()
