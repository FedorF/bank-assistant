import re
from typing import List, Optional, Tuple

from gensim import similarities
import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances_argmin_min


class QAModel:

    def __init__(
            self,
            path_to_data: str,
            n_closest: int,
            n_clusters: int,
            min_df: int,
    ):
        self.vectorizer = TfidfVectorizer(min_df=min_df)
        self.patterns = self._init_preprocessing_patterns()
        self.n_closest = n_closest
        self.n_clusters = n_clusters
        self.data = self._load_data(path_to_data)
        self.index, self.centroids, self.centroid_to_relevant, self.index_to_relevant = self._init_index(self.data)
        del self.data

    def _load_data(self, path_to_data: str) -> pd.DataFrame:
        df = pd.read_csv(path_to_data)[['question', 'answer']]
        df['index_'] = df.question.map(self._preprocess)
        df = df[df.index_.map(len) > 0]
        return df

    def _init_index(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, dict, dict]:
        index_ = self.vectorizer.fit_transform(data.index_.values)
        model = MiniBatchKMeans(n_clusters=self.n_clusters)
        model.fit(index_)
        centroids = model.cluster_centers_
        centroid_to_relevant = pairwise_distances_argmin_min(centroids, index_, metric='cosine')[0]
        centroid_to_relevant = {i: data.iloc[v, :2].values for i, v in enumerate(centroid_to_relevant)}
        index_to_relevant = {i: v for i, v in enumerate(data.iloc[:, :2].values)}
        return index_, model.cluster_centers_, centroid_to_relevant, index_to_relevant

    def _init_preprocessing_patterns(self) -> List:
        return [re.compile(r'[,!.;()?\'":<>/$*=%+-@&_]'), re.compile(r'\d+'), re.compile(r' +')]

    def _preprocess(self, query: str) -> Optional[str]:
        query = str(query).lower()
        for pattern in self.patterns:
            query = re.sub(pattern, ' ', query)

        query = query.strip()
        if query.isdigit():
            return np.nan

        return query

    def _vectorize(self, query: str) -> np.ndarray:
        return self.vectorizer.transform([query]).todense()

    def _find_closest(self, index: np.ndarray, query: np.ndarray, n_closest: int) -> List:
        index = similarities.SparseMatrixSimilarity(index, num_features=index.shape[1])
        relevant = index[query]
        relevant = sorted(enumerate(relevant), key=lambda item: -item[1])[:n_closest]
        return relevant

    def handle(self, query: str) -> Tuple[List, List]:
        query = self._preprocess(query)
        if not query:
            return [], []
        query = self._vectorize(query)

        candidates = []
        for candidate in self._find_closest(self.index, query, self.n_closest):
            relevant = self.index_to_relevant[candidate[0]]
            distance = candidate[1]
            candidates.append((relevant, distance))

        centroids = []
        for centroid in self._find_closest(self.centroids, query, self.n_closest):
            relevant = self.centroid_to_relevant[centroid[0]]
            distance = centroid[1]
            centroids.append((relevant, distance))

        return candidates, centroids
