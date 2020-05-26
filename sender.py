#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
import email

# TODO: iterate for each email in test folder
with open("test/test-2.eml", 'r') as mail_fd:
    mail_obj = email.message_from_file(mail_fd)
