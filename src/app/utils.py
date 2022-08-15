import dataclasses
import hashlib
from typing import Any, Dict


def get_hash(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()


def asdict(instance: Any) -> Dict:
    dataclasses.asdict(instance)
