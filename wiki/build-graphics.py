#!/usr/bin/env python3
"""후보 풀에 드는 에셋의 축소본을 만들고, 스튜디오의 생성 구간을 다시 쓴다.

  python3 wiki/build-graphics.py
  python3 wiki/build-graphics.py --check   쓰지 않고 어긋난 것만 알려준다

하는 일 세 가지.

  1. `assets.json` 의 `pools` 에 드는 원본(1400~5000px, 1~8MB)을 PX(긴 변) 로 줄여
     `studio/asset/<id>.png` 로 넣는다. PX 를 바꾸면 190장을 전부 다시 만든다.
  2. `studio/Main.dc.html` 의 CSS 생성 구간에 에셋마다 사용자 정의 속성을 쓴다.
         --g-g001: url("asset/g001.png");
  3. 같은 파일의 JS 생성 구간에 카탈로그(이름·절·검색어)와 후보 풀을 쓴다.

**왜 CSS 변수인가.** 아트보드 런타임은 마크업의 `src="이름.png"` 와 CSS 의
`url(이름.png)` 를 **글자 그대로 찾아** data: URI 로 바꿔 끼운다(이미지 확장자만).
`src="{{변수}}"` 처럼 값이 실행 중에 정해지는 자리는 바꿔 주지 않는다 — 실제로 시험해
깨지는 것을 확인했다. 그래서 그림은 CSS 변수로 미리 박아 두고, 코드는 변수 이름
(`var(--g-g001)`)만 골라 넘긴다. 이러면 studio/ 원본은 상대경로로, 번들은 data: URI 로
같은 마크업이 양쪽에서 돈다.

id 는 문서 순서에서 나오는 일련번호다. 사람에게 보이지 않고 어디에도 저장되지 않으므로,
인덱스에 줄이 끼어 번호가 밀려도 이 스크립트를 다시 돌리면 그만이다.
"""
import json, os, re, subprocess, sys, unicodedata as ud

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
OUT = os.path.join(ROOT, "studio", "asset")
MAIN = os.path.join(ROOT, "studio", "Main.dc.html")
# 긴 변 기준 축소 크기. 그리드는 48px, 원고의 그래픽 칸은 최대 196px 로 그린다.
# 220 에서 내렸다 — 번들이 9.6MB 였고, 190장을 base64 로 품은 값이라 여기가 곧 용량이다.
PX = 160
STAMP = "size.txt"            # 이 크기로 만들었다는 표시. 숫자를 바꾸면 전부 다시 만든다
N = lambda s: ud.normalize("NFC", s)

# 손으로 쓴 코드가 이름으로 집어야 하는 것들 — 기본 문서의 세 블록이 쓴다.
# 기본 문서가 쓰던 그림 그대로다. 'Coin_1/2' 는 이름과 달리 무늬 없는 흰 원반이고
# 금화 더미는 'Cash'(현금), 흰 선물상자는 'Gift Box 04' 다 — 이름만 보고 고르면 어긋난다.
ALIAS = {"apt": "아파트", "coin": "현금", "gift": "선물상자 4"}

CSS_HEAD = "    /* >>> 생성 구간 — wiki/build-graphics.py 가 쓴다. 손으로 고치지 않는다"
CSS_TAIL = "    /* <<< 생성 구간 */"
JS_HEAD = "  // >>> 생성 구간 — wiki/build-graphics.py 가 쓴다. 손으로 고치지 않는다"
JS_TAIL = "  // <<< 생성 구간"


def src_path(rel):
    p = os.path.join(ROOT, rel)
    return p if os.path.exists(p) else ud.normalize("NFD", p)


def label(row):
    f = row["fields"]
    return N(f.get("한글명") or f.get("슬롯") or f.get("기종")
             or (row["section"] + " " + f.get("번호", "")).strip())


def collect(data):
    """후보 풀에 한 번이라도 드는 에셋만, 문서 순서대로 id 를 매겨 모은다"""
    inpool = {"icon": set(), "illust": set(), "product": set()}
    for p in data["pools"].values():
        for kind in inpool:
            inpool[kind].update(p[kind])
    out, n = [], 0
    for kind in ("icon", "illust", "product"):
        for row in data[kind]:
            if row["section"] not in inpool[kind] or "목록 외" in row["section"]:
                continue
            n += 1
            out.append({"i": "g%03d" % n, "k": kind, "s": N(row["section"]),
                        "n": label(row), "t": " ".join(row["tags"]),
                        "src": row["paths"][0]})
    return out


def thumbs(items, check):
    """원본 → PX px PNG. 원본이 더 새것이거나 PX 가 바뀌었을 때만 다시 만든다"""
    os.makedirs(OUT, exist_ok=True)
    stamp = os.path.join(OUT, STAMP)
    resized = not (os.path.exists(stamp)
                   and open(stamp, encoding="utf-8").read().strip() == str(PX))
    made, stale, fail = 0, [], []
    for it in items:
        src, dst = src_path(it["src"]), os.path.join(OUT, it["i"] + ".png")
        if (not resized and os.path.exists(dst)
                and os.path.getmtime(dst) >= os.path.getmtime(src)):
            continue
        stale.append(it["i"])
        if check:
            continue
        r = subprocess.run(["sips", "-Z", str(PX), "-s", "format", "png", src, "--out", dst],
                           capture_output=True)
        if r.returncode:
            fail.append(it["src"])
        else:
            made += 1
    if not check:
        open(stamp, "w", encoding="utf-8").write(str(PX) + "\n")
    # 풀에서 빠진 에셋의 축소본은 지운다 — 번들에 유령이 남지 않게
    keep = {it["i"] + ".png" for it in items}
    gone = sorted(f for f in os.listdir(OUT) if f.endswith(".png") and f not in keep)
    if gone and not check:
        for f in gone:
            os.remove(os.path.join(OUT, f))
    return made, stale, gone, fail


def css_block(items):
    lines = [CSS_HEAD,
             "       그림은 여기 CSS 변수로만 들어온다. 이유는 wiki/build-graphics.py 머리말 */"]
    for it in items:
        lines.append('    :root { --g-%s: url("asset/%s.png"); }' % (it["i"], it["i"]))
    lines.append(CSS_TAIL)
    return "\n".join(lines)


def js_block(items, pools):
    def esc(s):
        return s.replace("\\", "\\\\").replace("'", "\\'")

    alias = {}
    for key, name in ALIAS.items():
        hit = [it for it in items if it["n"] == name]
        if not hit:
            sys.exit("ALIAS 의 '%s' 를 카탈로그에서 찾지 못했다 — 이름이 바뀌었는지 확인하라" % name)
        alias[key] = hit[0]["i"]

    lines = [JS_HEAD,
             "  // 카탈로그 %d개 · 후보 풀 %d종. 규칙은 wiki/template.md 2.5" % (len(items), len(pools)),
             "  gfxData() {",
             "    return {",
             "      alias: { " + ", ".join("%s: '%s'" % (k, v) for k, v in sorted(alias.items())) + " },",
             "      pool: {"]
    for cat, p in pools.items():
        cols = ", ".join("%s: [%s]" % (k, ", ".join("'" + esc(s) + "'" for s in p[k]))
                         for k in ("icon", "illust", "product"))
        lines.append("        '%s': { %s }," % (esc(cat), cols))
    lines.append("      },")
    lines.append("      gfx: [")
    for it in items:
        lines.append("        { i: '%s', k: '%s', s: '%s', n: '%s', t: '%s' },"
                     % (it["i"], it["k"], esc(it["s"]), esc(it["n"]), esc(it["t"])))
    lines += ["      ]", "    };", "  }", JS_TAIL]
    return "\n".join(lines)


def splice(text, head, tail, block, what):
    i = text.find(head)
    j = text.find(tail, i)
    if i < 0 or j < 0:
        sys.exit("Main.dc.html 에서 %s 생성 구간 표시를 찾지 못했다" % what)
    return text[:i] + block + text[j + len(tail):]


def main():
    check = "--check" in sys.argv
    data = json.load(open(os.path.join(WIKI, "assets.json"), encoding="utf-8"))
    if "pools" not in data:
        sys.exit("assets.json 에 pools 가 없다 — python3 wiki/build.py 를 먼저 돌려라")

    items = collect(data)
    # 도구는 6·7 을 한 카테고리로 쓴다 (template.md 2.5)
    pools = {k: {kk: list(v[kk]) for kk in ("icon", "illust", "product")}
             for k, v in data["pools"].items()}
    six, seven = pools.get("6. 서부 본부 전단"), pools.get("7. 유통망 요청 추가 유형 2")
    if six and seven:
        merged = {}
        for kk in ("icon", "illust", "product"):
            merged[kk] = six[kk] + [s for s in seven[kk] if s not in six[kk]]
        pools["6–7. 본부 · 유통망 요청"] = merged

    made, stale, gone, fail = thumbs(items, check)
    text = open(MAIN, encoding="utf-8").read()
    new = splice(text, CSS_HEAD, CSS_TAIL, css_block(items), "CSS")
    new = splice(new, JS_HEAD, JS_TAIL, js_block(items, pools), "JS")

    if check:
        drift = []
        if stale:
            drift.append("축소본 %d개가 원본보다 오래됐다" % len(stale))
        if gone:
            drift.append("풀에서 빠진 축소본 %d개가 남아 있다" % len(gone))
        if new != text:
            drift.append("Main.dc.html 생성 구간이 어긋난다")
        if drift:
            print("어긋남: " + " · ".join(drift))
            return 1
        print("일치 — 축소본 %d개와 생성 구간이 assets.json 과 같다" % len(items))
        return 0

    if fail:
        print("축소 실패 %d건:" % len(fail))
        for f in fail[:10]:
            print("   ", f)
        return 1
    if new != text:
        open(MAIN, "w", encoding="utf-8").write(new)

    total = sum(os.path.getsize(os.path.join(OUT, it["i"] + ".png")) for it in items)
    print("축소본 %d개 (%s) — 새로 만든 것 %d · 지운 것 %d"
          % (len(items), "%.1f MB" % (total / 1024 / 1024), made, len(gone)))
    kinds = {}
    for it in items:
        kinds[it["k"]] = kinds.get(it["k"], 0) + 1
    print("   " + " · ".join("%s %d" % (k, v) for k, v in kinds.items()))
    print("Main.dc.html 생성 구간 %s" % ("다시 씀" if new != text else "변경 없음"))
    print("\n다음: python3 wiki/sync-studio.py 로 번들에 반영한다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
