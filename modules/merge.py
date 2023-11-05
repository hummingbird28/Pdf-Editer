from . import *
from swibots import regexp, BotContext, CallbackQueryEvent

@Client.on_callback_query(regexp(r"merge"))
async def onCallback(ctx: BotContext[CallbackQueryEvent]):
    TASKS[ctx.event.action_by_id] = {"task": "merge"}
    message = "Send the pdf files you want to merge!"
    await ctx.event.message.delete()
    msg = ctx.event.message
    await msg.send(message)
