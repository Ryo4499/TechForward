# Tech Share Back End

## API単体での動作

docker-composeでportを開放します(例:5000)｡

```yaml
ports:
      - "0.0.0.0:5000:5000"
```

docker-composeの`command`を下記に変更します｡

```bash
flask run -h 0.0.0.0 -p 5000
```

こうすることで､単体での動作確認が出来ますが､DBを起動していないとエラーが発生します｡

## Portについて

コンテナ内のポートは5000で動作しています｡
DBのポートは.envを参照して下さい｡

## .envについて

.envがないとapiが起動しません｡
.env.sampleを.envという名前で./直下に複製してください｡

```bash
$ cd training-2021
$ cp .env.sample .env
```
