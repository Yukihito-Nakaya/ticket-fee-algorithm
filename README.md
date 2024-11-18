# ticket-fee-algorithm
Problem 1 Amount calculation program for zoo ticket sales operators

# 利用方法

cd ./src
pip install pyt
python manage.py calculation

### python 環境が無い場合
・docker pull python:3.11-slim
・sudo docker compose up --build






# 問題内容
## 【前提】
あなたは動物園のチケット販売オペレーター用金額計算プログラム作成を依頼されました。仕様は以下とする.

    ⚫︎ チケットの種類は以下とする
        ○ 入園チケット
        ○ どちらのタイプを適用するかは窓口で確認してオペレータが適切(か)は個別にプログラムのパラメーターとして指定する。
          （チラシ等を持ってきたら割引的な扱いと想定してください

| タイプ | 大人 | 子供 | シニア |
| 通常 | 1000 | 500 | 800 |
| 特別 | 600 | 400 | 500 |

    ⚫︎ 以下の条件のときに料金を変動させる。(特別タイプのチケットでも同様の条件で料金を変動させること)
        ○ 団体割引10人以上だと10%割引(子供は0.5人換算する)　※ 合計料金　× 0.9
        ○ 夕方料金夕方17時以降は100円引きする　※ 合計料金　- （タイプ人数合計　× 100）
        ○ 休日料金、休日は200円増　※ 合計料金　＋ （タイプ人数合計　× 200）
        ○ 月水割引月曜と水曜日は100円引きとする　※ 合計料金　- （タイプ人数合計　× 100）

    ⚫︎ 発生しうるエラーパターンについても十分考慮して適切に制御すること。
    ⚫︎ オペレータはPCのターミナルより該当プログラムの実行をする。
    ⚫︎ 出力結果には、最低限以下を表示すること。
        ○ 販売合計金額
        ○ 金額変更前合計金額
        ○ 金額変更明細

※ 四捨五入の条件がないため小数点以下は全て切り捨てます

## 【設問】
下記仕様に沿ったプログラムを作成してください。

### 補足
    ⚫︎ Pythonで作成したCLIプログラムとしてください。
    ⚫︎ Djangoのカスタムコマンドとして実装してください。
    ⚫︎ DBの利用は不可とします。
    ⚫︎ 使用上の疑問点や、不明点は質問として整理した上で、想定される回答を要して作成を進めてください。
    ⚫︎ 【可能であれば】今後チケットの種類や割引の種類の追加変更が発生する可能性があります。
        その際の改修しやすさについても十分検討してください。

## 【期待する成果物】
    ⚫︎ プログラム本体
    ⚫︎ テスト結果
    ⚫︎ 仕様に対する質問内容と想定回答（あれば）
