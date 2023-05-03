import argparse

from telegram import ext as tg

import config
from models import QAModel


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help='Deployment mode: dev or prod')
    return parser.parse_args()


def init_model(mode):
    if mode == 'prod':
        cfg = config.ProdConfig()
    else:
        cfg = config.DevConfig()
    return QAModel(cfg.PATH_TRAIN_SET, cfg.N_CLOSEST, cfg.N_CLUSTERS, cfg.MIN_DF)


args = parse_args()
model = init_model(args.mode)


def route_start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hello!")


def prepare_respond(model_output):
    candidates, centroids = model_output
    if (len(candidates) == 0) or (len(centroids) == 0):
        return 'Relevant Questions are not found'
    respond = 'Relevant Questions:\n'
    respond += '--------------------\n'
    for pair in candidates:
        respond += f'question : {pair[0][0]}\tanswer : {pair[0][1]}\tdistance : {pair[1]}\n'

    respond += '\nRelevant Clusters:\n'
    respond += '--------------------\n'
    for pair in centroids:
        respond += f'question : {pair[0][0]}\tanswer : {pair[0][1]}\tdistance : {pair[1]}\n'
    return respond


def handle_message(query):
    query = query.message.text.encode('utf-8')
    model_output = model.handle(query)
    respond = prepare_respond(model_output)
    return query.message.reply_text(respond)


def main():
    updater = tg.Updater(config.DevConfig.BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(tg.CommandHandler("start", route_start), group=0)
    dp.add_handler(tg.MessageHandler(tg.Filters.text, handle_message))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
