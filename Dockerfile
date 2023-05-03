FROM python:3.8-slim-buster

RUN mkdir -p binary/
COPY binary/tokens.json /binary/tokens.json
COPY binary/vk.csv /binary/vk.csv
COPY src/ /src
COPY requirements.txt /src/
WORKDIR /src

RUN python3 -m pip install -r requirements.txt

ENV MODE='prod'
ENV PATH_TRAIN_SET='../binary/vk.csv'
ENV TOKEN='5860894867:AAFRyNCLBQe7RaYxskHoRtdbnGENwP4gSsg'
ENV MIN_DF=5
ENV N_CLOSEST=3
ENV N_CLUSTERS=60

CMD python3 run_server.py --mode $MODE
