// サイト設定
window.SITE_CONFIG = {
  // 表示するシーズン（data/ 内のファイル名）
  season: "2026-10",
  // Supabase の Project URL と publishable key（公開して問題ないキー）
  supabaseUrl: "https://twasbricjiwjdqgrqcct.supabase.co",
  supabaseKey: "sb_publishable_RvpJHFQrCIYvGKR-YPO3sA_R4hAd2_f",

  // 注目ワードの初期値。閲覧者は画面の「注目ワード」から自分用に変更できます（変更はそのブラウザにだけ保存）
  // voiceActors: キャストに含まれていたら「注目」列に表示
  // keywords: タイトル・ポイント・監督・シリーズ構成・制作会社に含まれていたら表示
  watch: {
    voiceActors: ["早見沙織", "田村ゆかり", "諸星すみれ", "杉田智和", "内田真礼", "小倉唯", "花澤香菜", "芹澤優", "井口裕香", "東山奈央"],
    keywords: ["なろう", "アニオリ", "ジャンプ", "MAPPA", "Netflix", "ノイタミナ"]
  }
};
