FROM python:3.9.6

WORKDIR /api

COPY ./requirements.txt /api

RUN apt update && apt -y install locales && \
        localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV DOCKERIZE_VERSION v0.6.1
RUN apt-get update && apt-get install -y wget \
        && wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
        && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
        && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN pip install --upgrade pip \ 
        pip install --no-cache-dir -r /api/requirements.txt