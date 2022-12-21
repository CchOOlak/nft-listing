FROM python:3.9-alpine

RUN mkdir -p /code
ADD . /code

WORKDIR /code

RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

RUN apk add netcat-openbsd

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
