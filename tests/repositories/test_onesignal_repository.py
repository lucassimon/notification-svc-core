import pytest
import os
from unittest import mock

from notification_services.backends.onesignal.config import OneSignalConfig
from notification_services.backends.onesignal.entity import OneSignalPayloadRequest
from notification_services.backends.onesignal.onesignal_backend import (
    OneSignalBackendV1,
)
from notification_services.repositories.onesignal_repository import OneSignalRepository

from notification_services.services import Service


def test_onesignal_repository_constructor():
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )

    with mock.patch(
        "notification_services.repositories.onesignal_repository.OneSignalRepository.__init__",
        return_value=None,
    ) as Mocked:
        repo = OneSignalRepository(config=config, backend_klass=OneSignalBackendV1)
        Mocked.assert_called_with(config=config, backend_klass=OneSignalBackendV1)


def test_onesignal_repository_get_connection_with_backend_v3():
    """
    WHEN
        connection is none
        use_queue is False
    """
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )
    repo = OneSignalRepository(
        config=config, backend_klass=OneSignalBackendV1, connection=None
    )

    connection = repo.get_connection()

    assert isinstance(connection, OneSignalBackendV1)


def test_onesignal_repository_get_connection_raise_exception_when_use_queue_is_true():
    """
    WHEN
        connection is none
        use_queue is True
    """
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=True,
    )
    repo = OneSignalRepository(
        config=config, backend_klass=OneSignalBackendV1, connection=None
    )

    with pytest.raises(NotImplementedError) as e:
        connection = repo.get_connection()
        assert e == "TODO: Queue connection"


def test_onesignal_repository_get_connection_when_pass_argument_connection_on_contructor():
    fake_connection = "Fake Connection"
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )
    repo = OneSignalRepository(
        config=config,
        backend_klass=OneSignalBackendV1,
        connection=fake_connection,
    )

    connection = repo.get_connection()
    assert connection == fake_connection


def test_onesignal_repository_send_raise_value_error_when_email_message_is_empty():
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )
    repo = OneSignalRepository(
        config=config, backend_klass=OneSignalBackendV1, connection=None
    )
    with pytest.raises(ValueError) as e:
        repo.send(message=None)
        assert e == "Empty message"


def test_onesignal_repository_send_raise_value_error_when_email_message_is_not_mail_sendgrid_instance():
    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )
    repo = OneSignalRepository(
        config=config, backend_klass=OneSignalBackendV1, connection=None
    )
    with pytest.raises(ValueError) as e:
        repo.send(message={"foo": "bar"})
        assert e == "Message is not kind of Mail Sendgrid"


@mock.patch(
    "notification_services.backends.onesignal.onesignal_backend.OneSignalBackendV1.send",
    return_value="sent",
)
def test_onesignal_repository_send_is_sucessful(mocked):
    to = "+5531991256055"
    from_phone = "+15005550006"
    body = "hello world"

    message = OneSignalPayloadRequest(
        contents={"pt": "Ola mundo", "en": "Hello world"},
        headings={"pt": "Algum titulo", "en": "Some title"},
        included_segments=["Inactive Users"],
        data={"custom_data": "foo"},
        filters=[],
    )

    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )
    repo = OneSignalRepository(config=config, backend_klass=OneSignalBackendV1)
    response = repo.send(message=message)

    assert response == "sent"


def test_onesignal_repository_send_is_unsucessful():
    message = OneSignalPayloadRequest(
        contents={"pt": "Ola mundo", "en": "Hello world"},
        headings={"pt": "Algum titulo", "en": "Some title"},
        included_segments=["Inactive Users"],
        data={"custom_data": "foo"},
        filters=[],
    )

    config = OneSignalConfig(
        app_id=os.getenv("ONESIGNAL_APP_ID"),
        rest_api_key=os.getenv("ONESIGNAL_API_KEY"),
        user_auth_key=os.getenv("ONESIGNAL_AUTH_KEY"),
        use_queue=False,
    )

    with mock.patch(
        "notification_services.backends.onesignal.onesignal_backend.OneSignalBackendV1.send",
        side_effect=Exception("some-exception"),
    ) as ServiceMock:

        with pytest.raises(Exception) as e:
            repo = OneSignalRepository(config=config, backend_klass=OneSignalBackendV1)
            repo.send(message=message)

            assert e == "some-exception"
