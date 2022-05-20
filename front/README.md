# Tech Map Front End

## Portについて

コンテナ内のポートは8080で動作しています｡

## Build Setup

```bash
# 依存パッケージをインストールします｡
$ yarn install

# 開発用のサーバで起動します｡
$ yarn dev

# 本番用のサーバで起動します｡
$ yarn build
$ yarn start
```

[Nuxt.js 公式ドキュメント](https://nuxtjs.org).

## 各ディレクトリの内容について

各ディレクトリの内容について記載します｡

### `assets`

グローバルに適用されるSCSSのファイルやfontなどを置いてあります｡

### `components`

Vue コンポーネントを記載しています｡

### `layouts`

認証時ヘッダー､未認証ヘッダー､フッター､エラー画面のレイアウトを記載しています｡


### `pages`

各ページについて記載しています｡

### `plugins`

axios,vee-validate,logger,vuetifyの拡張設定を記載しています｡

### `static`

faviconを置いています｡

### `store`

nuxt-authモジュールの状態管理情報だけ記載しています(基本的に触る必要がないです)｡

