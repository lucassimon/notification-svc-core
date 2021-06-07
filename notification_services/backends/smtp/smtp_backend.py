import threading

from notification_services.backends.core import BaseEmailBackend
from .config import SmtpConfig


class SmtpBackendV1(BaseEmailBackend):
    def __init__(self, config: SmtpConfig, fail_silently=False):
        super().__init__(fail_silently=fail_silently)
        self.host = config.host
        self.port = config.port
        self.username = config.username
        self.password = config.password
        self.connection = None

    def open(self):

        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        try:
            self.connection = "conectar"
            return True
        except Exception as exc:
            raise exc

    def close(self):
        return False

    def send(self, email_messages):
        if not email_messages:
            return 0

        new_conn_created = self.open()
        if not self.connection or new_conn_created is None:
            # We failed silently on open().
            # Trying to send would be pointless.

            return 0

        num_sent = 0

        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1

        if new_conn_created:
            self.close()

        return num_sent

    def _send(self, email_message):
        print("private send mail from smtp_backend")
