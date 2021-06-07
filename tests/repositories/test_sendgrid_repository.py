import pytest
import os
from unittest import mock

from sendgrid.helpers.mail import Mail

from notification_services.services import Service
from notification_services.backends.sendgrid.config import SendgridConfig
from notification_services.backends.sendgrid.sendgrid_backend import SendgridBackendV3
from notification_services.repositories.sendgrid_repository import SendgridRepository


def test_sendgrid_repository_constructor():
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)

    with mock.patch(
        "notification_services.repositories.sendgrid_repository.SendgridRepository.__init__",
        return_value=None,
    ) as Mocked:
        some_repo = SendgridRepository(
            config=sendgrid_config, backend_klass=SendgridBackendV3
        )
        Mocked.assert_called_with(
            config=sendgrid_config, backend_klass=SendgridBackendV3
        )


def test_sendgrid_repository_get_connection_with_sendgrid_backend_v3():
    """
    WHEN
        connection is none
        use_queue is False
    """
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3, connection=None
    )

    connection = some_repo.get_connection()

    assert isinstance(connection, SendgridBackendV3)


def test_sendgrid_repository_get_connection_raise_exception_when_use_queue_is_true():
    """
    WHEN
        connection is none
        use_queue is True
    """
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=True)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3, connection=None
    )

    with pytest.raises(NotImplementedError) as e:
        connection = some_repo.get_connection()
        assert e == "TODO: Queue connection"


def test_sendgrid_repository_get_connection_when_pass_argument_connection_on_contructor():
    fake_connection = "Fake Connection"
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=True)
    some_repo = SendgridRepository(
        config=sendgrid_config,
        backend_klass=SendgridBackendV3,
        connection=fake_connection,
    )

    connection = some_repo.get_connection()
    assert connection == fake_connection


def test_sendgrid_repository_send_raise_value_error_when_email_message_is_empty():
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3, connection=None
    )
    with pytest.raises(ValueError) as e:
        some_repo.send(email_messages=None)
        assert e == "Empty message"


def test_sendgrid_repository_send_raise_value_error_when_email_message_is_not_mail_sendgrid_instance():
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3, connection=None
    )
    with pytest.raises(ValueError) as e:
        some_repo.send(email_messages={"foo": "bar"})
        assert e == "Message is not kind of Mail Sendgrid"


@mock.patch(
    "notification_services.backends.sendgrid.sendgrid_backend.SendgridBackendV3.send",
    return_value="sent",
)
def test_sendgrid_repository_send_is_sucessful():
    message = Mail(
        from_email="buzz@bar.com",
        to_emails="foo@bar.com",
        subject="test",
        html_content="<strong>test</strong>",
        amp_html_content="<strong>test</strong>",
        plain_text_content="test",
    )
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3
    )
    response = some_repo.send(email_messages=message)

    assert response == "senta"


def test_sendgrid_repository_send_is_sucessful():
    message = Mail(
        from_email="buzz@bar.com",
        to_emails="foo@bar.com",
        subject="test",
        html_content="<strong>test</strong>",
        amp_html_content="<strong>test</strong>",
        plain_text_content="test",
    )
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)

    with mock.patch(
        "notification_services.backends.sendgrid.sendgrid_backend.SendgridBackendV3.send",
        side_effect=Exception("some-exception"),
    ) as ServiceMock:

        with pytest.raises(Exception) as e:
            some_repo = SendgridRepository(
                config=sendgrid_config, backend_klass=SendgridBackendV3
            )
            some_repo.send(email_messages=message)

            assert e == "some-exception"
