from notification_services.backends.core import backend_factory, BaseNotificationBackend
from notification_services.backends.twilio.entity import TwilioPayloadRequest
from notification_services.backends.twilio.config import TwilioConfig

from .core import NotificationRepositoryInterface


class SMSTwilioRepository(NotificationRepositoryInterface):
    def __init__(
        self,
        config: TwilioConfig,
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

    def send(self, message: TwilioPayloadRequest):
        if not message:
            raise ValueError("Empty message")

        if not isinstance(message, TwilioPayloadRequest):
            raise ValueError("Message is not kind of Twilio Payload Request")

        connection = self.get_connection()

        try:
            return connection.send(message)
        except Exception:
            raise
