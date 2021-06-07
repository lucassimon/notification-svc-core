import pytest
import os
from unittest import mock

from twilio.base.exceptions import TwilioRestException

from notification_services.backends.twilio.config import TwilioConfig
from notification_services.backends.twilio.entity import TwilioPayloadRequest
from notification_services.backends.twilio.twilio_backend import TwilioBackendV1
from notification_services.repositories.sms_twilio_repository import SMSTwilioRepository

from notification_services.services import Service


def factory_message(to, from_phone, body):
    config = TwilioConfig(
        account_sid=os.environ.get("TWILIO_ACCOUNT_SID"),
        auth_token=os.environ.get("TWILIO_AUTH_TOKEN"),
        use_queue=False,
    )
    repo = SMSTwilioRepository(config=config, backend_klass=TwilioBackendV1)
    svc = Service(repo)

    # https://www.twilio.com/docs/iam/test-credentials
    message = TwilioPayloadRequest(to=to, from_phone=from_phone, body=body)

    response = svc.send(message)

    return response


def test_twilio_sms_service():
    to = "+5531991256055"
    from_phone = "+15005550006"
    body = "hello world"

    try:
        response = factory_message(to, from_phone, body)

    except Exception:
        raise


def test_twilio_sms_service_parameter_phone_number_is_unavailable():
    pass


def test_twilio_sms_service_parameter_phone_number_is_invalid():
    pass


def test_twilio_sms_service_parameter_area_code_does_not_have_any_available():
    pass


def test_twilio_sms_service_from_phone_number_is_invalid():
    to = "+5531991256055"
    body = "hello world"
    from_phone = "+15005550001"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_from_phone_number_is_not_owned_by_your_account():
    from_phone = "+15005550007"
    to = "+5531991256055"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_from_phone_number_queue_is_full():
    from_phone = "+15005550008"
    to = "+5531991256055"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_to_phone_number_is_invalid():
    to = "+15005550001"
    from_phone = "+15005550006"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_to_phone_number_twilio_cannot_route_to_this_number():
    to = "+15005550002"
    from_phone = "+15005550006"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_to_phone_number_your_account_does_not_have_the_international_permissions():
    to = "+15005550003"
    from_phone = "+15005550006"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_to_phone_number_the_number_is_blocked_for_your_account():
    to = "+15005550004"
    from_phone = "+15005550006"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )


def test_twilio_sms_service_to_phone_number_the_number_is_incapable_of_receiving_sms_messages():
    to = "+15005550009"
    from_phone = "+15005550006"
    body = "hello world"

    with pytest.raises(TwilioRestException) as e:
        response = factory_message(to, from_phone, body)

        assert (
            e.msg
            == "Unable to create record: The 'From' number +15005550001 is not a valid phone number, shortcode, or alphanumeric sender ID."
        )
