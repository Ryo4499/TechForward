# Tech Map

技術を共有するためのWebアプリケーションです｡

## ※.envがないと動きません

## 概要

技術共有システム

## .envについて

.envがないとapiが起動しません｡
/apiにて.env.sampleを.envという名前で/api直下に複製してください｡

```bash
cd training-2021
cp api/.env.sample api/.env
```

## 使い方

1. このリポジトリをクローンする

```bash
git clone git@github.com:systemsoft-ss1/training-2021.git
cd ./training-2021
```

2. プロジェクトのルートディレクトリでdocker-composeの実行

```bash
docker-compose up -d
```

3. localhost:80でnuxtアプリを起動


### 必要環境

* Docker
