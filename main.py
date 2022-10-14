from utils.credentials import (
    TOKEN_BOT_ANDOLINA_TEST,
    CHAT_ID_BOT,
    CHAT_ID_GROUP_COLEGIO_ANDOLINA,
)

from utils.constants import DOWNLOAD_FOLDER_BASE_PATH, TALK_TO_BOT
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def select_action_to_perform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if (chat_id == CHAT_ID_BOT) & (update.message.caption.startswith(TALK_TO_BOT)):
        # await echo(update, context)
        await download_document(update, context)


async def download_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.effective_message.document
    SAVING_DOCUMENT_PATH = DOWNLOAD_FOLDER_BASE_PATH + document.file_name
    file = await context.bot.get_file(document.file_id)
    await file.download(custom_path=SAVING_DOCUMENT_PATH)


async def action_for_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    chat_id = update.effective_chat.id
    if update.message.text.startswith(TALK_TO_BOT):
        await update.message.reply_text("You talk to a bot")




def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN_BOT_ANDOLINA_TEST).build()

    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, action_for_text_message))
    application.add_handler(MessageHandler(filters.Document.ALL & ~filters.COMMAND, select_action_to_perform))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

