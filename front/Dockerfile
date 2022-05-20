FROM node:14.17.4

WORKDIR /front

# カレントワーキングディレクトリ(つまり 'front' フォルダ)にプロジェクトのファイルやフォルダをコピーする
COPY ./package.json ./
COPY ./yarn.lock ./

# プロジェクトの依存ライブラリをインストールする
RUN yarn install
