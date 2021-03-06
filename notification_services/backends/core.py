def backend_factory(config, backend=None, fail_silently=False, **kwargs):
    return backend(config, fail_silently=fail_silently, **kwargs)


class BaseNotificationBackend:
    """
    Base class for notifications backend implementations.
    open() and close() can be called indirectly by using a backend object as a
    """

    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently

    def open(self):
        """
        Open a network connection.
        This method can be overwritten by backend implementations to
        open a network connection.
        It's up to the backend implementation to track the status of
        a network connection if it's needed by the backend.
        This method can be called by applications to force a single
        network connection to be used when sending notification.

        """
        pass

    def close(self):
        """Close a network connection."""
        pass

    def __enter__(self):
        try:
            self.open()
        except Exception:
            self.close()
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
