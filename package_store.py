import json
import os
from models import Package

STATE_FILE = os.environ.get("STATE_FILE", "/data/packages.json")


def load_packages(path: str) -> list[Package]:
    try:
        with open(path, encoding='utf-8') as f:
            raw = json.load(f)
            return [Package(**item) for item in raw]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_packages(path: str, packages: list[Package]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([p.model_dump(by_alias=True, mode="json") for p in packages], f)
        