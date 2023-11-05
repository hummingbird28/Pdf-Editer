from . import *
from glob import glob
from pypdf import PdfFileWriter
from secrets import token_hex
from helpers.splitPdf import split_pdf
from helpers.merge import mergeFiles
from swibots import regexp, BotContext, CallbackQueryEvent, CommandEvent


@Client.on_callback_query(regexp(r"process"))
async def processCommand(ctx: BotContext[CallbackQueryEvent]):
    user_id = ctx.event.action_by_id
    m = ctx.event.message
    if not TASKS.get(user_id):
        return
    task = TASKS[user_id]
    await ctx.event.message.delete()
    if task["task"] == "merge":
        file = mergeFiles(task["files"], f"merged_{user_id}.pdf", task.get("password"))
    elif task["task"] == "split":
        file = split_pdf(
            task["file"],
            f"{downloads}/{user_id}",
            start=task.get("start_page"),
            end=task.get("end_page"),
            password=task.get("password"),
        )
    else:
        return
    del TASKS[user_id]
    if os.path.isdir(file):
        files = glob(f"{file}/*")
    else:
        files = [file]
    for file in files:
        await m.send(
            message="PDF",
            document=file
        )
        os.remove(file)


@Client.on_command("split")
async def split_cmd(ctx: BotContext[CommandEvent]):
    message = m = ctx.event.message
    param = ctx.event.params
    start = end = None
    if param:
        try:
            split = param.split("-")
            start, end = int(split[0]), int(split[1])
        except (IndexError, ValueError):
            try:
                start = int(param)
            except ValueError:
                pass
    replied = await message.get_replied_message()
    if replied and replied.media_link.endswith(".pdf"):
        file = await replied.download(downloads)
        file = split_pdf(
            file,
            f"{downloads}/{message.user_id}",
            start=start,
            end=end,
        )
        if os.path.isdir(file):
            files = glob(f"{file}/*")
        else:
            files = [file]
        for file in files:
            await m.send(
            message="PDF",
            document=file
        )
            os.remove(file)
        return
    await message.send("Reply to a PDF!")
