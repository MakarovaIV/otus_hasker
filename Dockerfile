# syntax=docker/dockerfile:1

FROM debian

USER root

WORKDIR /app

RUN apt-get update

RUN apt-get install -y python3-pip python3-venv python3-dev libpq-dev git

RUN git clone https://github.com/MakarovaIV/otus_hasker.git

WORKDIR /app/otus_hasker

RUN pip install -r requirements.txt

RUN make prod

EXPOSE 5432
EXPOSE 80