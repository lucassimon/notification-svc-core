import pytest
import os
from unittest import mock

from sendgrid.helpers.mail import (
    Mail,
    From,
    To,
    Cc,
    Bcc,
    Subject,
    Substitution,
    Header,
    CustomArg,
    SendAt,
    Content,
    MimeType,
    Attachment,
    FileName,
    FileContent,
    FileType,
    Disposition,
    ContentId,
    TemplateId,
    Section,
    ReplyTo,
    Category,
    BatchId,
    Asm,
    GroupId,
    GroupsToDisplay,
    IpPoolName,
    MailSettings,
    BccSettings,
    BccSettingsEmail,
    BypassBounceManagement,
    BypassListManagement,
    BypassSpamManagement,
    BypassUnsubscribeManagement,
    FooterSettings,
    FooterText,
    FooterHtml,
    SandBoxMode,
    SpamCheck,
    SpamThreshold,
    SpamUrl,
    TrackingSettings,
    ClickTracking,
    SubscriptionTracking,
    SubscriptionText,
    SubscriptionHtml,
    SubscriptionSubstitutionTag,
    OpenTracking,
    OpenTrackingSubstitutionTag,
    Ganalytics,
    UtmSource,
    UtmMedium,
    UtmTerm,
    UtmContent,
    UtmCampaign,
)

from notification_services.backends.sendgrid.config import SendgridConfig
from notification_services.backends.sendgrid.sendgrid_backend import SendgridBackendV3
from notification_services.repositories.sendgrid_repository import SendgridRepository

from notification_services.services import Service


def factory_message(config, payload):
    message = Mail(
        from_email="cli@example.com",
        to_emails="lucassrod@gmail.com",
        subject="teste3",
        html_content="<strong>and easy to do anywhere, even with Python</strong>",
        amp_html_content="<strong>and easy to do anywhere, even with Python</strong>",
        plain_text_content="and easy to do anywhere, even with Python",
    )

    message.cc = [
        Cc("lucas.simon@ferreri.co", "Lucas Simon"),
    ]

    # if "bcc" in payload:
    #     message.bcc = [
    #         Bcc("test8@example.com", "Example User8"),
    #         Bcc("test9@example.com", "Example User9"),
    #     ]

    # if "header" in payload:
    #     message.header = [
    #         Header("X-Test3", "Test3"),
    #         Header("X-Test4", "Test4"),
    #     ]

    if "custom_arg" in payload:
        message.custom_arg = [
            CustomArg("x-request-id", "123"),
        ]

    # if "template_id" in payload:
    #     message.template_id = TemplateId("13b8f94f-bcae-4ec6-b752-70d6cb59f932")

    # mail_settings = MailSettings()
    # if config.spam_check:
    #     mail_settings.spam_check = SpamCheck(
    #         True,
    #         SpamThreshold(5),
    #     )

    # message.mail_settings = mail_settings

    # tracking_settings = TrackingSettings()
    # if config.tracking_check:
    #     tracking_settings.click_tracking = ClickTracking(True, True)
    #     tracking_settings.open_tracking = OpenTracking(
    #         True, OpenTrackingSubstitutionTag("open_tracking")
    #     )

    # if config.tracking_ganalytics:
    #     tracking_settings.ganalytics = Ganalytics(
    #         True,
    #         UtmSource("utm_source"),
    #         UtmMedium("utm_medium"),
    #         UtmTerm("utm_term"),
    #         UtmContent("utm_content"),
    #         UtmCampaign("utm_campaign"),
    #     )

    # message.tracking_settings = tracking_settings

    return message


def test_sendgrid_mail_service():
    try:
        api_key = os.getenv("SENDGRID_API_KEY")
        sendgrid_config = SendgridConfig(
            api_key=api_key, sandbox_mode=False, use_queue=False
        )
        sendgrid_repo = SendgridRepository(
            config=sendgrid_config, backend_klass=SendgridBackendV3
        )
        service_sendgrid = Service(sendgrid_repo)

        payload = {
            "from": {"email": "sam.smith@example.com", "name": "Sam Smith"},
            "to": [{"email": "sam.doe@example.com", "name": "Sam Doe"}],
            "bcc": [{"email": "sam.doe@example.com", "name": "Sam Doe"}],
            "cc": [{"email": "jane.doe@example.com", "name": "Jane Doe"}],
            "reply_to": {"email": "sam.smith@example.com", "name": "Sam Smith"},
            "subject": "some subject",
            "header": {
                "X-Service-Request-ID": "123",
                "X-Accept-Language": "en",
                "X-Mailer": "MyApp",
            },
            "custom_args": {
                "New Argument 1": "New Value 1",
                "activationAttempt": "1",
                "customerAccountNumber": "[CUSTOMER ACCOUNT NUMBER GOES HERE]",
            },
            "template_id": {
                "id": "[YOUR TEMPLATE ID GOES HERE]",
                "substitution": [
                    {"key": "%name4%", "value": "Example Name 4"},
                    {"key": "%city4%", "value": "Example Name 4"},
                ],
            },
            "ganalytics": {
                "utm_campaign": "[NAME OF YOUR REFERRER SOURCE]",
                "utm_content": "[USE THIS SPACE TO DIFFERENTIATE YOUR EMAIL FROM ADS]",
                "utm_medium": "[NAME OF YOUR MARKETING MEDIUM e.g. email]",
                "utm_name": "[NAME OF YOUR CAMPAIGN]",
                "utm_term": "[IDENTIFY PAID KEYWORDS HERE]",
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": "and easy to do anywhere, even with Python",
                },
                {
                    "type": "text/html",
                    "value": "<html><p>Hello, world!</p><img src=[CID GOES HERE]></img></html>",
                },
            ],
        }

        # email_messages_sendgrid = factory_message(
        #     config=sendgrid_config, payload=payload
        # )

        # response = service_sendgrid.send(email_messages_sendgrid)

    except Exception:
        raise
