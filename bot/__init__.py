import logging
logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger("bot")

from swibots import BotApp
from .loader import load_modules
from .config import Config

LOG.info("starting bot.")

Client = BotApp(
    Config.BOT_TOKEN,
    Config.BOT_DESCRIPTION
)

modules_path = Config.MODULES_PATH or "modules"
load_modules(modules_path)

__all__ = ["Client", "Config", "LOG"]