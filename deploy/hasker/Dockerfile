# syntax=docker/dockerfile:1

FROM debian

USER root

WORKDIR /app

RUN apt-get update

RUN apt-get install -y python3-pip python3-venv python3-dev libpq-dev git

RUN git clone https://github.com/MakarovaIV/otus_hasker.git hasker

WORKDIR /app/hasker

RUN pip install -r requirements.txt

RUN chmod 777 /app/hasker/deploy/hasker/start.sh

EXPOSE 8000