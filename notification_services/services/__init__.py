class Service:
    def __init__(self, repository):
        self.repository = repository

    def send(self, messages):
        try:
            return self.repository.send(messages)
        except Exception as exc:
            raise exc
