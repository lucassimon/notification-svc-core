import logging

from twilio.rest import Client
from twilio.base import exceptions


from notification_services.backends.core import BaseEmailBackend
from .config import TwilioConfig


class TwilioBackendV1(BaseEmailBackend):
    def __init__(self, config: TwilioConfig, fail_silently=False):
        super().__init__(fail_silently=fail_silently)
        self.config = config
        self.connection = None

    def open(self):
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        try:
            self.connection = Client(
                username=self.config.account_sid,
                password=self.config.auth_token,
            )
            if self.config.enable_log:
                logging.basicConfig(filename="./log.txt")
                self.connection.http_client.logger.setLevel(logging.INFO)
            return True
        except Exception as exc:
            raise exc

        except exceptions.UnauthorizedError:
            raise

    def close(self):
        return False

    def check_connection(self, new_conn_created):
        if not self.connection or new_conn_created is None:
            return False

        return True

    def send(self, message):

        new_conn_created = self.open()

        if not self.check_connection(new_conn_created):
            raise Exception("Could not create the connection")

        try:
            response = self.connection.messages.create(
                to=message.to, from_=message.from_phone, body=message.body
            )

            return response
        except exceptions.TwilioRestException as exc:
            raise exc
