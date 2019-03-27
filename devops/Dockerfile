FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

# RUN apk add postgresql-dev gcc python3-dev
RUN apk add --no-cache --virtual .build-deps \
                                ca-certificates \
                                gcc \
                                postgresql-dev \
                                linux-headers \
                                musl-dev \
                                libffi-dev \
                                jpeg-dev zlib-dev \
                                bash

WORKDIR /

ADD requirements /requirements

WORKDIR /requirements

RUN pip install -r base.txt
