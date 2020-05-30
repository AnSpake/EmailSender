#!/usr/bin/env python3
# pylint: disable=missing-docstring

import smtplib
import ssl


def fetch_email_addr(full_msg):
    """
        Fetch the addresse mail from Sender/To/From fields
    """
    return full_msg[full_msg.find('<') + 1:full_msg.find('>')]


class EmailClient():
    """
        Secure SMTP Client
    """

    def __init__(self, hostname, port, secure: bool = False):
        self.hostname = hostname
        self.port = port

        if secure:
            self.context = ssl.create_default_context()
            self.server = smtplib.SMTP_SSL(hostname,
                                           port,
                                           context=self.context)
        else:
            self.server = smtplib.SMTP(hostname, port)

    def sendmail(self, email_obj):
        """
            Wrapper for sendmail
        """
        if 'Attachment' in email_obj:
            self.handle_attachment(email_obj)
        self.server.sendmail(fetch_email_addr(email_obj['Sender']),
                             fetch_email_addr(email_obj['To']),
                             email_obj.as_string().encode("latin"))

    def handle_attachment(email_obj):
        """
            Parse attachment and include it in the email
        """
        pass

    def __enter__(self):
        return self

    def quit(self):
        """
            Close SMTP client
        """
        self.server.quit()

    def __exit__(self, exec_type, exec_value, traceback):
        self.quit()
