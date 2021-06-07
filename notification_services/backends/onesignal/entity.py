import json
from typing import Dict, List
from dataclasses import dataclass, field, InitVar, asdict


@dataclass(frozen=True)
class OneSignalPayloadRequest:
    headings: dict
    contents: dict
    included_segments: List[str]
    data: str
    filters: List

    def to_json(self) -> str:
        return asdict(self)
