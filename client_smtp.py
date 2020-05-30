#!/usr/bin/env python3
# pylint: disable=missing-docstring

import os
import ssl
import smtplib
from email.mime.application import MIMEApplication


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

    def sendmail(self, email_obj, subdir):
        """
            Wrapper for sendmail
        """
        if 'Attachment' in email_obj:
            self.handle_attachment(email_obj, subdir)
        self.server.sendmail(fetch_email_addr(email_obj['Sender']),
                             fetch_email_addr(email_obj['To']),
                             email_obj.as_string().encode("latin"))

    def handle_attachment(self, email_obj, subdir):
        """
            Parse attachment and include it in the email
        """
        # Every attachment are in the args.directory/attachment
        attach_path = os.path.join(subdir,
                                   "attachment",
                                   email_obj['Attachment'])
        _, attach_extension = os.path.splitext(attach_path)
        with open(attach_path, 'r') as attach_fd:
            attach_raw = MIMEApplication(attach_fd.read(),
                                         _subtype=attach_extension)
        attach_raw.add_header('Content-Disposition',
                              'attachment',
                              filename=email_obj['Attachment'])
        email_obj.attach(attach_raw)

    def __enter__(self):
        return self

    def quit(self):
        """
            Close SMTP client
        """
        self.server.quit()

    def __exit__(self, exec_type, exec_value, traceback):
        self.quit()
