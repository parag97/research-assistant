from pathlib import Path
from functools import cache

from core.config.loader import load_config
from core.config.models import Config


@cache
def get_config(path: str | Path = "configs/dev.yml") -> Config:
    return load_config(path)