FROM python:3.9-alpine

ARG UID
ARG GID
ARG USER
ARG GROUP
ARG DB_USER
ARG DB_PASS
ARG DB_HOST
ARG DB_NAME

RUN addgroup -g $GID $GROUP && adduser -G $GROUP -u $UID -D $USER

WORKDIR /api

COPY ./requirements.txt /api

RUN apk update && apk add -y --no-cache tzdata mariadb-connector-c-dev gcc musl-dev 


ENV DB_USER $DB_USER
ENV DB_PASS $DB_PASS
ENV DB_HOST $DB_HOST
ENV DB_NAME $DB_NAME
ENV LD_PRELOAD /usr/lib/mariadb/libmariadb.so
ENV LD_LIBRARY_PATH /usr/lib/mariadb
ENV TZ=Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
        && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
        && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN pip install --upgrade pip && pip install --no-cache-dir -r ./requirements.txt

RUN chown $USER:$GROUP -R ./ && unset UID GID GROUP

USER $USER

ENTRYPOINT ["dockerize","-timeout","30s","-wait","tcp://db:3306"] 
CMD ["gunicorn","--chdir", "./","--pythonpath","./","-b","127.0.0.1:5000", "run:app"]