#!/usr/bin/env python3
# pylint: disable=missing-module-docstring

import os
import sys
import email
import argparse
from client_smtp import EmailClient
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart


def handle_arg():
    """
        Parse CLI arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True,
                        help="The directory containing the emails to send")
    parser.add_argument('-p', '--port', required=False, type=int, default=2525,
                        help="SMTP client port")
    parser.add_argument('-s', '--servername', required=False, type=str,
                        default="localhost",
                        help="SMTP client servername")
    parser.add_argument('--ssl', required=False, action="store_true",
                        default=False,
                        help="Use a secure SMTP client")
    parser.add_argument('-a', '--attachment', required=False,
                        action="store_true", default=False,
                        help="Read attachment folder")

    args = parser.parse_args()
    return args


def main():
    """
        Run SMTP client to send multiple emails stocked in a directory
    """

    args = handle_arg()

    with EmailClient(args.servername, args.port, secure=args.ssl) as server:
        for subdir, _, files in os.walk(args.directory):
            for filename in files:
                with open(os.path.join(subdir, filename), 'r') as mail_fd:
                    mail_obj = email.message_from_file(mail_fd,
                                                       _class=EmailMessage)
                    # Add log
                    server.sendmail(mail_obj, subdir, args.attachment)


if __name__ == "__main__":
    sys.exit(main())
