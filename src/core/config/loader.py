from pathlib import Path

import yaml

from core.config.models import Config


def load_config(path: str | Path) -> Config:

    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return Config.model_validate(data)