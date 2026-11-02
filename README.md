# 雨通知プログラム

## 概要
- 天気予報を取得し、Discord に通知する
- 毎朝決まった時刻に、今日1日（0時〜23時）の降雨情報を届ける
- 朝のうちに、傘が必要な時間帯や洗濯物を干せる時間帯を確認できる

## できること
- 最高・最低気温、降水確率、天気を Discord に通知
- 降水確率が高い時間帯だけを一覧にして通知
- 「雨」とみなす降水確率を変更できる（初期値 50%）
- 雨の予報がない日は通知しない（オプションで毎日通知することもできる）
- 天気の取得や通知に失敗したときは、エラーを表示して終了する
- サーバー上で毎朝自動で実行

通知の例（雨の時間がある日）:

```
2026-11-02 東京：最高気温 20.3℃ /最低気温 12.5℃ /降水確率60% /天気：小雨
15:00 60%
16:00 70%
17:00 55%
```

通知の例（雨の予報がない日、`--always` を付けたとき）:

```
2026-11-01 東京：最高気温 20.3℃ /最低気温 12.5℃ /降水確率0% /天気：一部曇り
雨の予報はありません
```

## 使用技術
- Python 3.9（requests / python-dotenv / argparse）
- pytest（テスト）
- Open-Meteo API（天気予報データ）
- Discord Webhook（通知）
- AlmaLinux 9 / systemd timer（定期実行）
- Git / GitHub

## 構成
```
開発サーバー（コードを書く・テスト）
    │ git push
    ▼
GitHub
    │ git pull
    ▼
本番サーバー（systemd timer で毎朝 7:00 に実行）
    │
    ├─→ Open-Meteo API から天気予報を取得
    └─→ Discord Webhook で通知
```

- 本番では専用ユーザーで実行し、コードの書き換えはできないようにしている
- Webhook の URL は `.env` に保存し、Git には含めない

## セットアップ
```bash
git clone https://github.com/sutendr/weather.git
cd weather
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` の `DISCORD_WEBHOOK_URL=` のあとに、Discord で作成した Webhook の URL を書く。

## 使い方
```bash
python weather.py                  # 雨の時間があるときだけ通知
python weather.py --always         # 雨がなくても通知
python weather.py --threshold 30   # 降水確率 30% 以上を「雨」とみなす
python weather.py --help           # 使い方を表示
```

## テスト

```bash
pytest
```

雨の時間を抜き出す処理（`get_rain_hours`）をテストしている。

## 工夫した点
- **秘密情報を Git に入れない**: Webhook の URL は `.env` で管理し、エラーメッセージにも URL が出ないようにした
- **失敗に気づける**: 通信にタイムアウトを設定し、失敗したときは終了コード 1 で終わるようにした
- **処理を関数に分けた**: 取得・判定・送信を分け、判定の部分をテストできるようにした
- **本番の安全性**: 専用ユーザーで実行し、SELinux を有効にしたまま動くように配置した
- **開発と本番を分けた**: 本番では直接編集せず、GitHub 経由でだけ更新する

## 今後の予定
- Docker でコンテナ化
- GitHub Actions で自動テスト
- 通知の見た目の改善（雨の時間を先頭にまとめる、Discord の Embed を使う）

## 天気データについて
天気予報データは [Open-Meteo](https://open-meteo.com/) を利用しています（CC BY 4.0）。
Open-Meteo の無料 API は非商用利用に限られます。

