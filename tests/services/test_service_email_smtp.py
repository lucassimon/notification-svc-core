import pytest
import os
from unittest import mock

from notification_services.backends.smtp.config import SmtpConfig
from notification_services.backends.smtp.smtp_backend import SmtpBackendV1
from notification_services.repositories.smtp_repository import SmtpRepository

from notification_services.services import Service


def test_mail_service():
    try:
        email_messages_smtp = [1, 2, 3]
        smtp_config = SmtpConfig(
            host="localhost", port="25010", username="", password=""
        )
        smtp_repo = SmtpRepository(config=smtp_config, backend_klass=SmtpBackendV1)
        service_smtp = Service(smtp_repo)

        response = service_smtp.send(email_messages_smtp)

    except Exception:
        raise
