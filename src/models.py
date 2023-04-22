import re
import pickle
from typing import List, Tuple

from gensim import similarities
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min


class QAModel:

    def __init__(self, n_closest: int):
        self.vectorizer = TfidfVectorizer(min_df=5)
        self.patterns = self._init_preprocessing_patterns()
        self.n_closest = n_closest
        self.index, self.centroids = self._init_index()

    def _init_index():

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

    def _init_preprocessing_patterns(self):
        return [re.compile(r'[,!.;()?\'":<>/$*=%+-@&_]'), r'\d+', r' +']

    def _init_model(self):
        features = vectorizer.fit_transform(texts)

    try:
        centroids = pickle.load(open(PATH_TO_KM_CENTROIDS, "rb"))

    except (OSError, IOError) as e:
        print('Starting K-means')
        K = 50
        km = KMeans(n_clusters=K).fit(features)
        centroids = km.cluster_centers_
        closest = pairwise_distances_argmin_min(centroids, features, metric='cosine')  # Эталонные
        pickle.dump(centroids, open(PATH_TO_KM_CENTROIDS, 'wb'))
        print('Finishing K-means')

    def _preprocess(self, query: str):
        for pattern in self.patterns:
            query = re.sub(pattern, ' ', query)

        query = query.decode('utf-8').lower()
        query = self.vectorizer.transform([query]).todense()
        return query

    def _find_closest(self, index, query, n_closest):
        index = similarities.SparseMatrixSimilarity(index, num_features=index.shape[1])
        relevant = index[query]
        relevant = sorted(enumerate(relevant), key=lambda item: -item[1])[:n_closest]
        return relevant

    def handle(self, query: str) -> List[Tuple[str, str]]:
        query = self._preprocess(query)
        answer = []
        for relevant in self._find_closest(self.index, query, self.n_closest):
            answer.append((self.index[relevant[0]], relevant[1]))

        for centroid in self._find_closest(self.centroids, query, self.n_closest):
            answer.append((self.index[centroid[0]], centroid[1]))

        return answer
