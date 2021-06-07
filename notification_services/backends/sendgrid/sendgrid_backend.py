from sendgrid import SendGridAPIClient

from python_http_client import exceptions

from notification_services.backends.core import BaseEmailBackend
from .config import SendgridConfig


class SendgridBackendV3(BaseEmailBackend):
    def __init__(self, config: SendgridConfig, fail_silently=False):
        super().__init__(fail_silently=fail_silently)
        self.config = config
        self.connection = None

    def open(self):
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        try:
            self.connection = SendGridAPIClient(self.config.api_key)
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

    def send(self, email_messages):

        new_conn_created = self.open()

        if not self.check_connection(new_conn_created):
            raise Exception("Could not create the connection")

        try:
            response = self.connection.send(email_messages)
            return response
        except (
            exceptions.BadRequestsError,
            exceptions.ForbiddenError,
            exceptions.NotFoundError,
            exceptions.MethodNotAllowedError,
            exceptions.PayloadTooLargeError,
            exceptions.UnsupportedMediaTypeError,
            exceptions.TooManyRequestsError,
            exceptions.InternalServerError,
            exceptions.ServiceUnavailableError,
            exceptions.GatewayTimeoutError,
        ) as exc:
            raise exc
