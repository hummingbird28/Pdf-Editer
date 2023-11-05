import os
from swibots import BotCommand
from bot import Client, Config

downloads = Config.DOWNLOADS_PATH or "downloads"
if not os.path.exists(downloads):
    os.mkdir(downloads)

TASKS = {}

Client.set_bot_commands(
    [
        BotCommand("start", "Get start message", True),
        BotCommand("split", "split pdf (reply to media)", True),
        BotCommand("cancel", "Cancel ongoing task", True),
    ]
)
