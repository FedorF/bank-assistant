# coding: utf-8
# more examples: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/README.md
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from gensim import similarities
import pandas as pd
import re
import pickle

TG_TOKEN = "1234567890sdfghjkl;349sdfghjd2567e8r"
TG_TOKEN_TO_MY_BOT = "459584154:AAHDGyBupOEUcl6-0drHxh7uDWMPI8fpkGE"

PATH_TO_DATA = "/home/fed/Documents/sberTask/vk.csv"
PATH_TO_KM_CENTROIDS = "/home/fed/Documents/sberTask/km_pickle/km"


data = pd.read_csv(PATH_TO_DATA, sep=',')
data.question = data.question.str.lower()
data.question = data.question.str.replace(r'[,!.;()?\'":<>/$*=%+-@&_]', ' ')
data.question = data.question.str.replace(r'\d+', ' ')
data.question = data.question.str.replace(r' +', ' ')
data.question = data.question.str.strip()
data.dropna(axis=0, how='any', inplace=True)
data = data.reset_index(drop=True)
texts = data.question

data_original = pd.read_csv(PATH_TO_DATA, sep=',')
data_original.dropna(axis=0, how='any', inplace=True)
data_original = data_original.reset_index(drop=True)

vectorizer = TfidfVectorizer(min_df=5)
features = vectorizer.fit_transform(texts)

try:
    centroids = pickle.load(open(PATH_TO_KM_CENTROIDS, "rb"))

except (OSError, IOError) as e:

    print('Starting K-means')
    K = 50
    km = KMeans(n_clusters=K).fit(features)
    centroids = km.cluster_centers_
    closest = pairwise_distances_argmin_min(centroids, features, metric='cosine') # Эталонные
    pickle.dump(centroids, open(PATH_TO_KM_CENTROIDS, 'wb'))
    print ('Finishing K-means')



def preprocess_q(t):

    t = re.sub(r'[,!.;()?\'":<>/$*=%+-@&_]', ' ', t)
    t = re.sub(r'\d+', ' ', t)
    t = re.sub(r' +', ' ', t)
    t = t.decode('utf-8').lower()
    return vectorizer.transform([t]).todense()

def findClosest(to, question):
    index = similarities.SparseMatrixSimilarity(to, num_features=to.shape[1])
    sims = index[question]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return sims[:5]





def idle_main(bot, update):

    print ('idle_main')
    question = update.message.text.encode('utf-8')
    sims = findClosest(features, preprocess_q(question))
    sims_label = findClosest(centroids, preprocess_q(question))
    l = []
    for i in range(5):
        l.append(data_original.question[sims[i][0]])
        l.append(data_original.answer[sims[i][0]])
        l.append(str(sims[i][1]))
    for i in range(5):
        l.append(data_original.question[sims_label[i][0]])
        l.append(str(sims_label[i][1]))
    update.message.reply_text('\n'.join(l))


def slash_start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hello!")


def main():

    updater = Updater(TG_TOKEN_TO_MY_BOT)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", slash_start), group=0)
    dp.add_handler(MessageHandler(Filters.text, idle_main))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
