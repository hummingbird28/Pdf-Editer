import os
from swibots import BotContext, CommandEvent
from . import Client, TASKS

@Client.on_command("cancel")
async def cancelTask(ctx: BotContext[CommandEvent]):
    user = ctx.event.user.id
    if TASKS.get(user):
        for file in TASKS[user].get("files", []):
            os.remove(file)
        del TASKS[user]
        await ctx.event.message.reply_text("Ended Task!")
        return
    await ctx.event.message.reply_text("No task is currently running!")