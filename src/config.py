import os

from pydantic import BaseSettings

from utils import load_json


class DevConfig(BaseSettings):
    PATH_TRAIN_SET: str = '../binary/vk.csv'
    TOKEN: str = load_json('../binary/tokens.json')['token']
    N_CLUSTERS: int = 60
    N_CLOSEST: int = 3
    MIN_DF: int = 5


class ProdConfig(BaseSettings):
    PATH_TRAIN_SET: str = os.environ['PATH_TRAIN_SET']
    TOKEN: str = os.environ['TOKEN']
    MIN_DF: int = os.environ['MIN_DF']
    N_CLOSEST: int = os.environ['N_CLOSEST']
    N_CLUSTERS: int = os.environ['N_CLUSTERS']
