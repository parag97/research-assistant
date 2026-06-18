from core.config.service import get_config


config = get_config()
print(config.model_dump())