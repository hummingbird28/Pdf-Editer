from . import *
from swibots import BotContext, InlineMarkup, InlineKeyboardButton, CallbackQueryEvent, regexp

# @Client.on_callback_query(regexp(r"split$"))
async def onCallback(ctx: BotContext[CallbackQueryEvent]):
    msg = ctx.event.message
    await msg.edit_text(
        "Select the output file format",
        inline_markup=InlineMarkup(
            [
                [
                    InlineKeyboardButton("PDF", callback_data="split_pdf"),
                    InlineKeyboardButton("JPEG", callback_data="split_jpeg"),
                ]
            ]
        ),
    )


@Client.on_callback_query(regexp(r"split"))  # regexp(r"split_(.*)"))
async def splitFormat(ctx: BotContext[CallbackQueryEvent]):
    msg = ctx.event.message
    format = "pdf"
#    print(ctx.event.callback_data)
    TASKS[ctx.event.action_by_id] = {"task": "split"}
    await msg.edit_text(f"Send the PDF file to split into `{format}`")


@Client.on_callback_query(regexp(r"asksplit$"))
async def askSplit(ctx: BotContext[CallbackQueryEvent]):
    user = ctx.event.action_by_id
#    print(ctx.event.callback_data)
    if not TASKS.get(user):
        return
    task = TASKS[user]
    task["wait"] = "ASK_START"
    await ctx.event.message.delete()
    await ctx.event.message.send("Provide the start page number:")
