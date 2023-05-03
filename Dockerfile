FROM python:3.8-slim-buster

COPY binary/ /binary
COPY src/ /src
WORKDIR /src

RUN python3 -m pip install -r requirements.txt
RUN unzip binary/vk.csv.zip -d binary/vk.csv

CMD python3 run_server.py --mode prod
