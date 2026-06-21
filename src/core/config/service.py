from functools import cache
from pathlib import Path

from core.config.loader import load_config
from core.config.models import Config

# Default config path relative to the project root.
# Override by passing an explicit path to get_config().
_DEFAULT_CONFIG_PATH = "configs/dev.yml"


@cache
def get_config(path: str | Path = _DEFAULT_CONFIG_PATH) -> Config:
    """
    Load and cache the application configuration.

    Results are memoised — repeated calls with the same path return the
    same Config instance without re-reading or re-parsing the file.

    Parameters
    ----------
    path : Path to the YAML config file. Defaults to configs/dev.yml.
    """

    return load_config(path)
