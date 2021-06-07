from sendgrid.helpers.mail import Mail

from notification_services.backends.core import backend_factory, BaseNotificationBackend
from notification_services.backends.sendgrid.config import SendgridConfig

from .core import NotificationRepositoryInterface


class SendgridRepository(NotificationRepositoryInterface):
    def __init__(
        self,
        config: SendgridConfig,
        backend_klass: BaseNotificationBackend,
        connection=None,
    ):
        self.config = config
        self.connection = connection
        self.backend_klass = backend_klass

    def get_connection(self, fail_silently=False):
        if not self.connection and not self.config.use_queue:
            self.connection = backend_factory(
                self.config, self.backend_klass, fail_silently=fail_silently
            )
        elif not self.connection and self.config.use_queue:
            # conexao com o sistema de filas
            # TODO: Implementar um sistema de conexao com filas para os seguintes sistemas:
            # - RabbitMQ, NATs, Kafka....
            raise NotImplementedError("TODO: Queue connection")
        return self.connection

    def send(self, email_messages: Mail, fail_silently=False):
        if not email_messages:
            raise ValueError("Empty message")

        if not isinstance(email_messages, Mail):
            raise ValueError("Message is not kind of Mail Sendgrid")

        connection = self.get_connection(fail_silently=fail_silently)

        try:
            return connection.send(email_messages)
        except Exception:
            raise
