from typing import Dict
from dataclasses import dataclass, field, InitVar


@dataclass(frozen=True)
class SendgridConfig:
    api_key: str
    sandbox_mode: bool = field(default=False)
    spam_check: bool = field(default=False)
    tracking_check: bool = field(default=False)
    tracking_ganalytics: bool = field(default=False)
    use_queue: bool = field(default=False)
