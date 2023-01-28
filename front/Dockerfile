FROM node:16-alpine as dev-env

ARG UID
ARG GID

ENV TZ=Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

WORKDIR /front

# プロジェクトの依存ライブラリをインストールする
RUN apk update && apk add -y --no-cache tzdata python3 make gcc g++
COPY --chown=node:node ./package.json ./
COPY --chown=node:node ./yarn.lock ./

RUN yarn install 

COPY --chown=node:node . .

CMD ["yarn", "dev"]

FROM node:16-alpine

ARG UID
ARG GID

ENV TZ=Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

WORKDIR /front

# プロジェクトの依存ライブラリをインストールする
RUN apk update && apk add -y --no-cache tzdata python3 make gcc g++
RUN chown -R node:node ./
COPY --chown=node:node . .

USER node 
RUN yarn install 

RUN yarn build && yarn cache clean

CMD ["yarn", "start"]