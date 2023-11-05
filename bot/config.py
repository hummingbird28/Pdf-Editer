from typing import Any
from decouple import config

class ConfigHandler:
    BOT_TOKEN: str= config("BOT_TOKEN", default="", cast=str) # type: ignore
    MONGO_URL: str = config("MONGO_URL", default="", cast=str) # type: ignore

    def __getattribute__(self, __name: str) -> Any:
        return config(__name, default="")

Config = ConfigHandler()