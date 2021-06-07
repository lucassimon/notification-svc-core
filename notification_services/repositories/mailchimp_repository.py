from .core import NotificationRepositoryInterface


class MailChimpRepository(NotificationRepositoryInterface):
    def __init__(self, connection=None):

        self.connection = connection

    def get_connection(self):

        return self.connection

    def send(self, message, fail_silently=False):
        connection = self.get_connection()

        try:
            return connection.send(message)
        except Exception:
            raise
