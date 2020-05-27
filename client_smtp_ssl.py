#!/usr/bin/env python3

import smtplib, ssl

def fetch_email_addr(full_msg):
    return full_msg[full_msg.find('<') + 1:full_msg.find('>')]

class EmailClient():
    """
        Secure SMTP Client
    """

    def __init__(self, hostname, port, enable_ssl : bool =False):
        self.hostname = hostname
        self.port = port

        if enable_ssl:
            self.context = ssl.create_default_context()
            self.server = smtplib.SMTP_SSL(hostname, port, context=self.context)
        else:
            self.server = smtplib.SMTP(hostname, port)

    def sendmail(self, email_obj):
        self.server.sendmail(fetch_email_addr(email_obj['Sender'])
                            , fetch_email_addr(email_obj['To'])
                            , email_obj.as_string())

    def __enter__(self):
        return self

    def quit(self):
        self.server.quit()

    def __exit__(self, exec_type, exec_value, tb):
        self.quit()
