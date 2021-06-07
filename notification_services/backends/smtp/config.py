from typing import Dict
from dataclasses import dataclass, field, InitVar


@dataclass(frozen=True)
class SmtpConfig:
    host: str
    port: str
    username: str
    password: str
