from . import *

from swibots import BotContext, CommandEvent, InlineKeyboardButton, InlineMarkup

START_MESSAGE = """
Hi *{name}*, I am Pdf Utility Bot.

Select any of the below option to continue..."""


@Client.on_command("start")
async def onClientStart(ctx: BotContext[CommandEvent]):
    await ctx.event.message.reply_text(
        START_MESSAGE.format(name=ctx.event.user.name),
        inline_markup=InlineMarkup(
            [
                [
                    InlineKeyboardButton("Merge PDFs", callback_data="merge"),
                    InlineKeyboardButton("Split PDF", callback_data="split"),
                ]
            ]
        ),
    )
