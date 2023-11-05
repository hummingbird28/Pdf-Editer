from . import *
from pypdf import PdfReader
from swibots import BotContext, MessageEvent, InlineKeyboardButton, InlineMarkup


@Client.on_message()
async def messageListener(ctx: BotContext[MessageEvent]):
    message = ctx.event.message
    user_id = message.user.id
    if not TASKS.get(user_id):
        return
    task = TASKS[user_id]
    if task.get("task") == "split" and task.get("wait"):
        try:
            param = int(message.message)
        except (TypeError, ValueError):
            param = None
        if not param:
            return
        if task["wait"] == "ASK_START":
            task["start_page"] = param
            await message.reply_text("Provide the end page number:")
            task["wait"] = "ASK_END"
            return
        elif task["wait"] == "ASK_END":
            task["end_page"] = param
            await message.reply_text(
                "Click the Below button",
                inline_markup=InlineMarkup(
                    [[InlineKeyboardButton("Start", callback_data="process")]]
                ),
            )
            return
    if task.get("last_msg_id"):
        await ctx.delete_message(task["last_msg_id"])
    if not message.media_link:
        return
    isPdf = message.media_link.endswith(".pdf")
    isImage = message.media_link.endswith((".jpg", ".png", ".jpeg"))
    if task["task"] == "split" and isImage:
        return
    if isPdf or isImage:
        file = await message.download(downloads)
        if task["task"] in ["split"]:
            task["file"] = file
        else:
            if not task.get("files"):
                task["files"] = []
            task["files"].append(file)
        baseName = os.path.basename(file)
        with open(file, "rb") as f:
            reader = PdfReader(f)
            totalPages = len(reader.pages)
            fileInfo = reader.metadata
        keyboard = []
        if task["task"] == "split":
            keyboard.append(
                [InlineKeyboardButton("Choose Start-End", callback_data="asksplit")]
            )
        keyboard.append(
            [InlineKeyboardButton("Start Process", callback_data="process")]
        )
        message = await message.reply_text(
            f"Added `{baseName}` to the {task['task']} queue.\n*Title:* {fileInfo.title if fileInfo else 'Untitled'}"
            + f"\n*Pages*: {totalPages}",
            inline_markup=InlineMarkup(keyboard),
        )
        task["last_msg_id"] = message.id
