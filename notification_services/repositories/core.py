import abc


class NotificationRepositoryInterface:
    __metaclass__ = abc.ABCMeta

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "send") and callable(subclass.send) or NotImplemented

    @abc.abstractmethod
    def send(self):
        """Send email"""
        raise NotImplementedError
