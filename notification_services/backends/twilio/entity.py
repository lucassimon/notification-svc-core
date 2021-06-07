from typing import Dict
from dataclasses import dataclass, field, InitVar


@dataclass(frozen=True)
class TwilioPayloadRequest:
    to: str
    from_phone: str
    body: str


@dataclass(frozen=True)
class TwilioPayloadResponse:
    account_sid: str
    api_version: str
    body: str
    date_created: str
    date_sent: str
    date_updated: str
    direction: str
    error_code: any
    error_message: any
    from_phone: str
    messaging_service_sid: any
    num_media: str
    num_segments: str
    price: str
    price_unit: str
    sid: str
    status: str
    subresource_uris: any
    media: str
    to: str
    uri: str
