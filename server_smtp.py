#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=fixme

import sys
import asyncore
from secure_smtpd import SMTPServer


class EmailServer(SMTPServer):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.server = None

    def start(self):
        self.server = SMTPServer(localaddr=(self.hostname, self.port),
                                 remoteaddr=(self.hostname, self.port),
                                 ssl=True,
                                 certfile="localhost.pem",
                                 keyfile="localhost-key.pem")
        asyncore.loop()

    # TODO: investigate
    # def process_message(self, peer, mailfrom, rcpttos, message_data):
    #    print(message_data)


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
