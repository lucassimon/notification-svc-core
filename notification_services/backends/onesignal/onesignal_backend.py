import logging

from onesignal_sdk.client import Client
from onesignal_sdk.error import OneSignalHTTPError


from notification_services.backends.core import BaseEmailBackend

from .config import OneSignalConfig


class OneSignalBackendV1(BaseEmailBackend):
    def __init__(self, config: OneSignalConfig, fail_silently=False):
        super().__init__(fail_silently=fail_silently)
        self.config = config
        self.connection = None

    def open(self):
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        try:
            self.connection = Client(
                app_id=self.config.app_id,
                rest_api_key=self.config.rest_api_key,
                user_auth_key=self.config.user_auth_key,
            )
            if self.config.enable_log:
                logging.basicConfig(filename="./log.txt")
                self.connection.http_client.logger.setLevel(logging.INFO)
            return True
        except Exception as exc:
            raise exc

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
            response = self.connection.send_notification(message)

            return response
        except OneSignalHTTPError as exc:
            raise exc
