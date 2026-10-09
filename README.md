# アニメ視聴検討表

今期アニメの一覧に、原作・制作・放送局のポイント、PV・Wikipediaへのリンク、「観る／様子見／割愛」の投票を付けた静的サイトです。

## ファイル
- `index.html` … サイト本体
- `config.js` … 表示するシーズンと Supabase の接続先
- `data/YYYY-MM.json` … シーズンごとの作品データ
- `supabase.sql` … 投票用のテーブルと関数（Supabase の SQL Editor で1回実行）

## 毎期の更新
1. `data/` に新しいシーズンのJSONを追加（例：`2027-01.json`）
2. `config.js` の `season` を書き換える

投票はシーズンごとに分かれて保存されます。
