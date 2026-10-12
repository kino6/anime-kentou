"""原作情報（tools/sources_YYYY-MM.py）を作品データの source と point に反映する。
使い方: python3 tools/build_points.py 2026-10
原作の掲載先と掲載年数は必須。開始年が分からないものは「要確認」と表示し、最後に一覧を出す。"""
import json, re, sys, importlib.util
season = sys.argv[1]
THIS_YEAR = int(season[:4])
spec = importlib.util.spec_from_file_location("src", f"tools/sources_{season}.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
S = mod.SOURCES
path = f"data/{season}.json"
d = json.load(open(path, encoding="utf-8"))

ORIG_HINT = re.compile(r"漫画|コミック|文庫|ジャンプ|マガジン|サンデー|なろう|ゲーム|絵本|原作|原案|WEBTOON|スピリッツ|ポラリス|ヤンマガ|ガルパン|アイカツ|ウマ娘|IdentityV|ヴァンガード|ゲルぴよ|シルバニア|鉄道むすめ|ショートギャグ|小説|日向夏|続編|特撮|前作|図鑑|オリジナル|再放送|特別篇|タヌキ役|地上波|Ankama|フラッパー|LaLa|ジャンプ|アワーズ|Plott|SNS")

def period(s, e, kind):
    if s is None: return "開始年は要確認"
    if e == "-": return f"{s}年" + ("（新作）" if s >= THIS_YEAR else f"発売・発表（{THIS_YEAR - s}年前）")
    if e is None:
        n = THIS_YEAR - s
        return f"{s}年〜継続中（{n}年目）" if n == 0 else f"{s}年〜継続中（{n}年）"
    n = e - s
    return f"{s}〜{e}年 完結（{n}年）" if n else f"{s}年 完結（1年未満）"

def text(src):
    kind, venue, pub, s, e, note = src
    if kind in ("オリジナル", "アニメ再編集"):
        t = f"原作なし（{pub}）"
        if kind == "アニメ再編集": t = f"原作：{pub}"
    elif kind == "不明":
        t = f"原作：要確認（{pub}）"
    else:
        where = f"『{venue}』" if venue else ""
        t = f"原作：{kind}{where}" + (f"（{pub}）" if pub else "") + "、" + period(s, e, kind)
    return t + (f"。{note}" if note else "")

missing = []
for it in d["items"]:
    src = S[it["id"]]
    kind, venue, pub, s, e, note = src
    it["source"] = {"kind": kind, "venue": venue, "publisher": pub, "start": s,
                    "end": ("single" if e == "-" else e), "note": note}
    old = it.get("point_extra")
    if old is None:
        p = it["point"]
        first, _, rest = p.partition("。")
        old = rest if (rest and ORIG_HINT.search(first)) else (p if not ORIG_HINT.search(first) else "")
        it["point_extra"] = old.strip("。")
    it["point"] = text(src) + ("。" + it["point_extra"] if it["point_extra"] else "")
    if (s is None or kind == "不明") and kind not in ("オリジナル",):
        missing.append(f'{it["id"]} {it["title"]}')
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for it in d["items"]: print(it["id"], it["point"])
print("\n要確認:", len(missing)); print("\n".join(missing))
