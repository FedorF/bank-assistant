import os
from pathlib import Path

from pydantic import BaseSettings


class DevConfig(BaseSettings):
    PATH_TRAIN_SET: Path = Path('./binary/vk.csv.zip')
    PATH_CENTROIDS: Path = Path('./binary/centroids')
    BOT_TOKEN = ...
    TG_TOKEN = ...


class ProdConfig(BaseSettings):
    PATH_TRAIN_SET: Path = os.environ['PATH_TRAIN_SET']
    PATH_CENTROIDS: Path = os.environ['PATH_CENTROIDS']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    TG_TOKEN = os.environ['TG_TOKEN']
