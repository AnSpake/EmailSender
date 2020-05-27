#!/usr/bin/env python3

import email
from client_smtp_ssl import EmailClient

# TODO: Launch SMTP server
# python -m smtpd -n -c DebuggingServer localhost:465
smtp_hostname = "localhost"
smtp_port = 465

with EmailClient(smtp_hostname, smtp_port, enable_ssl=False) as server:
    # TODO: iterate for each email in test folder
    with open("test/test-2.eml", 'r') as mail_fd:
        mail_obj = email.message_from_file(mail_fd)
        # Add log
        server.sendmail(mail_obj)
