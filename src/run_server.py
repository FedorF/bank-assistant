from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config
from models import QAModel

model = QAModel(config.DevConfig)


def slash_start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hello!")


def process_query(query):
    query = query.message.text.encode('utf-8')
    respond = model.handle(query)
    respond = query.message.reply_text('\n'.join(respond))
    return respond


def main():
    updater = Updater(config.DevConfig.BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", slash_start), group=0)
    dp.add_handler(MessageHandler(Filters.text, process_query))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
