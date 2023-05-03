import os
from pathlib import Path

from pydantic import BaseSettings

from utils import load_json


class DevConfig(BaseSettings):
    PATH_TRAIN_SET: str = Path('../binary/vk.csv')
    BOT_TOKEN: str = load_json('../binary/tokens.json')['bot']
    TG_TOKEN: str = load_json('../binary/tokens.json')['telegram']
    N_CLUSTERS: int = 60
    N_CLOSEST: int = 5
    MIN_DF: int = 5


class ProdConfig(BaseSettings):
    PATH_TRAIN_SET: str = os.environ['PATH_TRAIN_SET']
    BOT_TOKEN: str = os.environ['BOT_TOKEN']
    TG_TOKEN: str = os.environ['TG_TOKEN']
    MIN_DF: int = os.environ['MIN_DF']
    N_CLOSEST: int = os.environ['N_CLOSEST']
    N_CLUSTERS: int = os.environ['N_CLUSTERS']
