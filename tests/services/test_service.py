import pytest
import os
from unittest import mock

from sendgrid.helpers.mail import Mail

from notification_services.services import Service
from notification_services.backends.sendgrid.config import SendgridConfig
from notification_services.backends.sendgrid.sendgrid_backend import SendgridBackendV3
from notification_services.repositories.sendgrid_repository import SendgridRepository


def test_mail_service_constructor():
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3
    )
    with mock.patch(
        "notification_services.services.Service.__init__",
        return_value=None,
    ) as ServiceMock:
        Service(some_repo)
        ServiceMock.assert_called_with(some_repo)


def test_mail_service_send_with_mail_argument():
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3
    )
    message = Mail(
        from_email="cli@example.com",
        to_emails="lucassrod@gmail.com",
        subject="teste3",
        html_content="<strong>and easy to do anywhere, even with Python</strong>",
        amp_html_content="<strong>and easy to do anywhere, even with Python</strong>",
        plain_text_content="and easy to do anywhere, even with Python",
    )
    with mock.patch(
        "notification_services.services.Service.send",
        return_value="some-response",
    ) as ServiceMock:
        sv = Service(some_repo)

        response = sv.send(message)
        ServiceMock.assert_called_with(message)

        arguments_tuple = ServiceMock.call_args[0]

        assert message in arguments_tuple
        assert "some-response" == response


def test_mail_service_send_raises_an_exception():
    sendgrid_config = SendgridConfig(api_key="", sandbox_mode=False, use_queue=False)
    some_repo = SendgridRepository(
        config=sendgrid_config, backend_klass=SendgridBackendV3
    )

    with mock.patch(
        "notification_services.repositories.sendgrid_repository.SendgridRepository.send",
        side_effect=Exception("some-exception"),
    ) as ServiceMock:

        with pytest.raises(Exception) as e:
            sv = Service(some_repo)
            sv.send("some-message")

            assert e == "some-exception"
