# Tech Forward Back End

## API単体での動作

docker-composeでportを開放します(例:5000)｡

```yaml
ports:
      - "127.0.0.1:5000:5000"
```

docker-composeの`command`を下記に変更します｡

```bash
flask run -h 127.0.0.1 -p 5000
```

こうすることで､単体での動作確認が出来ますが､DBを起動していないとエラーが発生します｡

## Portについて

コンテナ内のポートは5000で動作しています｡
DBのポートは.envを参照して下さい｡

## .envについて

.envがないとapiが起動しません｡
.env.sampleを.envという名前で./直下に複製してください｡

```bash
$ cd TechForward
$ cp .env.sample .env
```
