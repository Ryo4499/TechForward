# Tech Forward

技術を共有するためのWebアプリケーションです｡

## ※.envがないと動きません

## 概要

技術共有システム

## .envについて

.envがないとapiが起動しません｡
.env.sampleを.envという名前で./直下に複製してください｡

```bash
cd TechForward
cp ./.env.sample .env
```

## 使い方

1. このリポジトリをクローンする

```bash
git clone git@github.com:Ryo4499/TechForward.git
cd ./TechForward
```

2. プロジェクトのルートディレクトリでdocker-composeの実行

```bash
docker-compose up -d
```

3. localhost:80でnuxtアプリを起動


### 必要環境

* Docker
