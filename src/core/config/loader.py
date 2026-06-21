from pathlib import Path

import yaml

from core.config.models import Config


def load_config(path: str | Path) -> Config:
    """
    Load and validate a YAML config file into a Config object.

    Parameters
    ----------
    path : Path to the YAML configuration file (e.g. "configs/dev.yml").

    Returns
    -------
    Config : Validated Pydantic model populated from the file contents.

    Raises
    ------
    FileNotFoundError  : If the file does not exist at the given path.
    ValidationError    : If the YAML contents fail Pydantic validation.
    """

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return Config.model_validate(data)
