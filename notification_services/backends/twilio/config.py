from typing import Dict
from dataclasses import dataclass, field, InitVar


@dataclass(frozen=True)
class TwilioConfig:
    account_sid: str
    auth_token: str
    edge: str = field(default="sao-paulo")
    region: str = field(default="br1")
    enable_log: bool = field(default=False)
    use_queue: bool = field(default=False)
