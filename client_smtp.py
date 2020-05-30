#!/usr/bin/env python3
# pylint: disable=missing-docstring

import os
import ssl
import smtplib
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def fetch_email_addr(full_msg):
    """
        Fetch the addresse mail from Sender/To/From fields
    """
    return full_msg[full_msg.find('<') + 1:full_msg.find('>')]


def mail_to_multipart(mail):
    """
        Convert EmailMessage to MIMEMultipart in order to
        avoid "Attach is not valid on a message with a non-multipart
        payload"
    """
    if mail.is_multipart():
        return mail

    mail_multi = MIMEMultipart("mixed")
    headers = list((key, var) for (key, var) in mail.items()
                   if key not in
                   ("Content-Type", "Content-Transfer-Encoding"))

    for key, var in headers:
        mail_multi[key] = var
        del mail[key]

    mail_multi.attach(mail)
    return mail_multi


def handle_mime_type(main_type, sub_type, path):
    """
        Open and read attachment file differently depending on
        their types
    """
    if main_type == "text":
        with open(path, 'r') as attach_fd:
            attach_raw = MIMEText(attach_fd.read())
    else:
        with open(path, 'rb') as attach_fd:
            if main_type == "image":
                attach_raw = MIMEImage(attach_fd.read(), _subtype=sub_type)
            elif main_type == "audio":
                attach_raw = MIMEAudio(attach_fd.read(), _subtype=sub_type)
            elif main_type == "application":
                attach_raw = MIMEApplication(attach_fd.read(), _subtype=sub_type)
            else:
                attach_raw = MIMEBase(main_type, sub_type)
                attach_raw.set_payload(attach_fd.read())
                encoders.encode_base64(attach_raw)
    return attach_raw


def handle_attachment(email_obj, directory):
    """
        Parse attachment and include it in the email
    """
    # Every attachment are in the args.directory/attachment
    attach_path = os.path.join(directory,
                               "attachment",
                               email_obj['Attachment'])
    mime_type, encoding = mimetypes.guess_type(attach_path)
    if mime_type is None or encoding is not None:
        mime_type = "application/octet-stream"

    main_type, sub_type = mime_type.split('/', 1)

    attach_raw = handle_mime_type(main_type, sub_type, attach_path)

    email_obj.attach(attach_raw)


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

    def sendmail(self, email_obj, args):
        """
            Wrapper for sendmail
        """
        if args.attachment:
            email_obj = mail_to_multipart(email_obj)
            handle_attachment(email_obj, args.directory)
        self.server.sendmail(fetch_email_addr(email_obj['Sender']),
                             fetch_email_addr(email_obj['To']),
                             email_obj.as_string().encode("latin"))

    def __enter__(self):
        return self

    def quit(self):
        """
            Close SMTP client
        """
        self.server.quit()

    def __exit__(self, exec_type, exec_value, traceback):
        self.quit()
