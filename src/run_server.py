import argparse

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import config
from models import QAModel


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help='Deployment mode: dev or prod')
    return parser.parse_args()


def load_config(mode):
    if mode == 'prod':
        return config.ProdConfig()
    return config.DevConfig()


def init_model(conf):
    return QAModel(conf.PATH_TRAIN_SET, conf.N_CLOSEST, conf.N_CLUSTERS, conf.MIN_DF)


args = parse_args()
conf = load_config(args.mode)
model = init_model(conf)


def route_start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hello!")


def prepare_respond(model_output):
    candidates, centroids = model_output
    if (len(candidates) == 0) or (len(centroids) == 0):
        return 'Relevant Questions are not found'
    respond = 'Relevant Questions:\n'
    for pair in candidates:
        respond += f'question : {pair[0][0]}\nanswer : {pair[0][1]}\ndistance : {round(pair[1], 2)}\n\n'

    respond += '\nRelevant Clusters:\n'
    for pair in centroids:
        respond += f'question : {pair[0][0]}\nanswer : {pair[0][1]}\ndistance : {round(pair[1], 2)}\n\n'
    return respond


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive user's query and respond with relevant Q&A pairs."""
    model_output = model.handle(update.message.text)
    respond = prepare_respond(model_output)
    await update.message.reply_text(respond)


def main():
    application = Application.builder().token(conf.TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()


if __name__ == '__main__':
    main()
