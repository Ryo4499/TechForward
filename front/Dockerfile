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

# カレントワーキングディレクトリ(つまり 'front' フォルダ)にプロジェクトのファイルやフォルダをコピーする
COPY --chown=node:node ./package.json ./
COPY --chown=node:node ./yarn.lock ./

RUN yarn install && yarn build && yarn cache clean

COPY --chown=node:node . .

RUN chown node:node -R ./ && unset UID GID GROUP

USER node 

CMD ["yarn","start"]