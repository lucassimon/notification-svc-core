from typing import Dict
from dataclasses import dataclass, field, InitVar


@dataclass(frozen=True)
class OneSignalConfig:
    app_id: str
    rest_api_key: str
    user_auth_key: str
    enable_log: bool = field(default=False)
    use_queue: bool = field(default=False)
