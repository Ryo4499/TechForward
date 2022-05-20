# Tech Map

社内で技術を共有するためのWebアプリケーションです｡

## 概要

新人研修2021の開発研修

## .envについて

.envがないとapiが起動しません｡
/apiにて.env.sampleを.envという名前で/api直下に複製してください｡

```bash
$ cd training-2021
$ cp api/.env.sample api/.env
```

## 使い方

1. このリポジトリをクローンする

```bash
$ git clone git@github.com:systemsoft-ss1/training-2021.git
$ cd ./training-2021
```

2. プロジェクトのルートディレクトリでdocker-composeの実行

```bash
$ docker-compose up -d
```

3. localhost:80でnuxtアプリを起動


### 必要環境

* Docker

## ルーティング

詳細は\新人研修2021\開発研修\ドキュメント内の仕様.mdに記載


