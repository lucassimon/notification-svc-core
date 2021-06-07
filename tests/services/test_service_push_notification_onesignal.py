import pytest
import os
from unittest import mock

from onesignal_sdk.error import OneSignalHTTPError

from notification_services.backends.onesignal.config import OneSignalConfig
from notification_services.backends.onesignal.entity import OneSignalPayloadRequest
from notification_services.backends.onesignal.onesignal_backend import (
    OneSignalBackendV1,
)
from notification_services.repositories.onesignal_repository import OneSignalRepository

from notification_services.services import Service


def factory_svc():
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )
    repo = OneSignalRepository(config=config, backend_klass=OneSignalBackendV1)
    svc = Service(repo)

    return svc


def test_onesignal_push_notification_service_sucessful():
    svc = factory_svc()

    message = OneSignalPayloadRequest(
        contents={"pt": "Ola mundo", "en": "Hello world"},
        headings={"pt": "Algum titulo", "en": "Some title"},
        included_segments=["Inactive Users"],
        data={"custom_data": "foo"},
        filters=[],
    )
    response = svc.send(message)
