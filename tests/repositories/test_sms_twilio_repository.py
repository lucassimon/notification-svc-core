import pytest
import os
from unittest import mock

from sendgrid.helpers.mail import Mail

from twilio.base.exceptions import TwilioRestException

from notification_services.backends.twilio.config import TwilioConfig
from notification_services.backends.twilio.entity import TwilioPayloadRequest
from notification_services.backends.twilio.twilio_backend import TwilioBackendV1
from notification_services.repositories.sms_twilio_repository import SMSTwilioRepository


def test_sms_twilio_repository_constructor():
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )

    with mock.patch(
        "notification_services.repositories.sms_twilio_repository.SMSTwilioRepository.__init__",
        return_value=None,
    ) as Mocked:
        repo = SMSTwilioRepository(config=config, backend_klass=TwilioBackendV1)
        Mocked.assert_called_with(config=config, backend_klass=TwilioBackendV1)


def test_sms_twilio_repository_get_connection_with_backend_v3():
    """
    WHEN
        connection is none
        use_queue is False
    """
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )
    repo = SMSTwilioRepository(
        config=config, backend_klass=TwilioBackendV1, connection=None
    )

    connection = repo.get_connection()

    assert isinstance(connection, TwilioBackendV1)


def test_sms_twilio_repository_get_connection_raise_exception_when_use_queue_is_true():
    """
    WHEN
        connection is none
        use_queue is True
    """
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=True,
    )
    repo = SMSTwilioRepository(
        config=config, backend_klass=TwilioBackendV1, connection=None
    )

    with pytest.raises(NotImplementedError) as e:
        connection = repo.get_connection()
        assert e == "TODO: Queue connection"


def test_sms_twilio_repository_get_connection_when_pass_argument_connection_on_contructor():
    fake_connection = "Fake Connection"
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=True,
    )
    repo = SMSTwilioRepository(
        config=config,
        backend_klass=TwilioBackendV1,
        connection=fake_connection,
    )

    connection = repo.get_connection()
    assert connection == fake_connection


def test_sms_twilio_repository_send_raise_value_error_when_email_message_is_empty():
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )
    repo = SMSTwilioRepository(
        config=config, backend_klass=TwilioBackendV1, connection=None
    )
    with pytest.raises(ValueError) as e:
        repo.send(message=None)
        assert e == "Empty message"


def test_sms_twilio_repository_send_raise_value_error_when_email_message_is_not_mail_sendgrid_instance():
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )
    repo = SMSTwilioRepository(
        config=config, backend_klass=TwilioBackendV1, connection=None
    )
    with pytest.raises(ValueError) as e:
        repo.send(message={"foo": "bar"})
        assert e == "Message is not kind of Mail Sendgrid"


@mock.patch(
    "notification_services.backends.twilio.twilio_backend.TwilioBackendV1.send",
    return_value="sent",
)
def test_sms_twilio_repository_send_is_sucessful(mocked):
    to = "+5531991256055"
    from_phone = "+15005550006"
    body = "hello world"

    message = TwilioPayloadRequest(to=to, from_phone=from_phone, body=body)

    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )
    repo = SMSTwilioRepository(config=config, backend_klass=TwilioBackendV1)
    response = repo.send(message=message)

    assert response == "sent"


def test_sms_twilio_repository_send_is_unsucessful():
    to = "+5531991256055"
    from_phone = "+15005550006"
    body = "hello world"
    message = TwilioPayloadRequest(to=to, from_phone=from_phone, body=body)

    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )

    with mock.patch(
        "notification_services.backends.twilio.twilio_backend.TwilioBackendV1.send",
        side_effect=Exception("some-exception"),
    ) as ServiceMock:

        with pytest.raises(Exception) as e:
            repo = SMSTwilioRepository(config=config, backend_klass=TwilioBackendV1)
            repo.send(message=message)

            assert e == "some-exception"
