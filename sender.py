#!/usr/bin/env python3
# pylint: disable=missing-module-docstring

import sys
import email
import argparse
from client_smtp_ssl import EmailClient

# TODO: Launch SMTP server
# python -m smtpd -n -c DebuggingServer localhost:465
SMTP_HOSTNAME = "localhost"
SMTP_PORT = 465


def handle_arg():
    """
        Parse CLI arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True,
                        help="The directory containing the emails to send")

    args = parser.parse_args()
    return args


def main():
    """
        Run SMTP client to send multiple emails stocked in a directory
    """

    args = handle_arg()

    with EmailClient(SMTP_HOSTNAME, SMTP_PORT, enable_ssl=False) as server:
        # TODO: iterate for each email in test folder
        with open("test/test-2.eml", 'r') as mail_fd:
            mail_obj = email.message_from_file(mail_fd)
            # Add log
            server.sendmail(mail_obj)

if __name__ == "__main__":
    sys.exit(main())
