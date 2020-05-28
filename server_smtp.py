#!/usr/bin/env python3

import sys
import asyncore
from secure_smtpd import SMTPServer


class EmailServer(SMTPServer):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.server = SMTPServer((self.hostname, self.port),
                                 (self.hostname, self.port),
                                 ssl=True,
                                 certfile="localhost.pem",
                                 keyfile="localhost-key.pem")
        asyncore.loop()

    def process_message(self, peer, mailfrom, rcpttos, message_data):
        print(message_data)

    def quit(self):
        self.server.quit()


def main():
    """
        Run SMTP Server
    """

    hostname = "localhost"
    port = 2525

    server = EmailServer(hostname, port)
    server.start()


if __name__ == "__main__":
    sys.exit(main())
