from notification_services.backends.smtp.config import SmtpConfig
from notification_services.backends.core import backend_factory, BaseNotificationBackend

from .core import NotificationRepositoryInterface


class SmtpRepository(NotificationRepositoryInterface):
    def __init__(
        self,
        config: SmtpConfig,
        backend_klass: BaseNotificationBackend,
        connection=None,
    ):
        self.config = config
        self.connection = connection
        self.backend_klass = backend_klass

    def get_connection(self, fail_silently=False):
        if not self.connection:
            self.connection = backend_factory(
                self.config, self.backend_klass, fail_silently=fail_silently
            )
        return self.connection

    def send(self, email_messages, fail_silently=False):
        connection = self.get_connection(fail_silently=fail_silently)
        connection.send(email_messages)
