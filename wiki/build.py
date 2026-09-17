#!/usr/bin/env python3
"""wiki/*.md 의 표를 읽어 assets.json 을 생성하고, 파일 경로를 전부 검증한다.

  python3 wiki/build.py

표의 셀에서 `백틱`으로 감싼 파일 참조를 모은다. 참조는 두 가지로 적을 수 있다.
  - `line-001.png`                     → 그 문서의 기본 폴더 기준
  - `../brand guide/2D Icon/png/x.png` → wiki/ 기준 상대경로

검색어(태그)는 두 군데에서 온다. 둘 다 있으면 합친다.
  - 표의 `검색어` 열        → 행 단위. 에셋마다 다른 아이콘·제품컷이 쓴다
  - 섹션의 `> 검색어: …` 줄 → 섹션 단위. 한 섹션이 통째로 한 묶음인 인물 일러스트가 쓴다

후보 풀(pools)은 template.md 2.5 의 표에서 온다. 블록 카테고리마다 그래픽 슬롯에
올 수 있는 섹션을 한정한다. 표에 적힌 섹션 이름이 인덱스에 없으면 빌드가 실패한다 —
경로를 검증하는 것과 같은 이유다.

macOS는 한글 파일명을 NFD(자모 분리)로 저장한다. 위키 문서는 NFC로 적히므로
단순 문자열 비교로는 전부 "없는 파일"이 된다. N() 이 그 차이를 흡수한다.
"""
import json, os, re, sys, unicodedata as ud

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
N = lambda s: ud.normalize("NFC", s)
EXT = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".svg", ".woff2", ".otf", ".pdf", ".ai")

SRC = {
    "icon":    ("assets-icon.md",      "brand guide/3D Icon"),
    "illust":  ("assets-illust.md",    "brand guide/3D Illustration"),
    "product": ("assets-product.md",   "brand guide/Product Photography"),
    "lineicon":("assets-line-icon.md", "brand guide/Line Icon/png"),
    "font":    ("typography.md",       "brand guide/font/web"),
    "logo":    ("assets-logo.md",      "brand guide/logo"),
}

# 후보 풀 — template.md 2.5 의 표. 열 이름 → assets.json 의 종류 키
POOL_MD = "template.md"
POOL_COLS = {"3D 아이콘 섹션": "icon", "인물 일러스트": "illust", "제품컷": "product"}

def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def is_rule(c):
    return all(re.fullmatch(r":?-{2,}:?", x) for x in c)

def resolve(ref, default_folder):
    """참조 문자열 → 프로젝트 루트 기준 상대경로"""
    if "/" in ref:
        return os.path.normpath(os.path.join("wiki", ref))
    return os.path.join(default_folder, ref)

def tags_of(text):
    """검색어 셀·줄 → 낱말 목록. 빈칸 표시 '—' 는 버린다"""
    return [t for t in N(text or "").split() if t and t != "—"]

def parse(path, folder):
    out, head, section, sec_tags = [], None, None, []
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if line.startswith("#"):
            section, head, sec_tags = N(line.lstrip("#").strip()), None, []
            continue
        if line.startswith(">"):
            m = re.match(r">\s*검색어\s*[:：]\s*(.+)", line)
            if m:
                sec_tags = tags_of(m.group(1))
            continue
        if not line.startswith("|"):
            continue
        c = cells(line)
        if is_rule(c):
            continue
        if head is None:
            head = c
            continue
        refs = [N(r) for r in re.findall(r"`([^`]+)`", line) if r.lower().endswith(EXT)]
        if not refs:
            continue
        fields = dict(zip(head, c))
        tags = list(sec_tags)
        for t in tags_of(fields.get("검색어", "")):
            if t not in tags:
                tags.append(t)
        out.append({"section": section,
                    "fields": fields,
                    "tags": tags,
                    "paths": [resolve(r, folder) for r in refs]})
    return out

def usable(rows):
    """'목록 외' 섹션은 BX팀 미확인이라 후보에서 뺀다"""
    return [r for r in rows if "목록 외" not in (r["section"] or "")]

def parse_pools(data, errs):
    """template.md 2.5 의 표 → {카테고리: {icon|illust|product: [섹션…], n: 수}}"""
    pools, head = {}, None
    for raw in open(os.path.join(WIKI, POOL_MD), encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.startswith("|"):
            head = None
            continue
        c = cells(line)
        if head is None:
            head = c if "블록 카테고리" in c and "3D 아이콘 섹션" in c else False
            continue
        if head is False or is_rule(c):
            continue
        f = dict(zip(head, c))
        key = N(f["#"] + ". " + f["블록 카테고리"])
        entry, n = {}, 0
        for col, kind in POOL_COLS.items():
            rows = usable(data.get(kind, []))
            have = []
            for r in rows:                                  # 문서 순서를 지킨다
                if r["section"] not in have:
                    have.append(r["section"])
            v = N(f[col])
            names = [] if v == "—" else (have if v == "전체" else
                                         [s.strip() for s in v.split("·")])
            for s in names:
                if s not in have:
                    errs.append(f"{POOL_MD} 2.5  {key}  →  {kind} 에 '{s}' 섹션이 없다")
            entry[kind] = names
            n += len([r for r in rows if r["section"] in names])
        entry["n"] = n
        pools[key] = entry
    return pools

def main():
    data, missing, total = {}, [], 0
    for kind, (md, folder) in SRC.items():
        mdp = os.path.join(WIKI, md)
        if not os.path.exists(mdp):
            print(f"  ! {md} 없음"); continue
        rows = parse(mdp, folder)
        for r in rows:
            for p in r["paths"]:
                total += 1
                if not os.path.exists(N(os.path.join(ROOT, p))):
                    missing.append(f"{md}  →  {p}")
        data[kind] = rows

    bad = []
    pools = parse_pools(data, bad)

    json.dump(dict(data, pools=pools), open(os.path.join(WIKI, "assets.json"), "w"),
              ensure_ascii=False, indent=1)

    tagged = sum(len([r for r in v if r["tags"]]) for v in data.values())
    print(f"assets.json 생성 — {sum(len(v) for v in data.values())}행 / 파일참조 {total}건 / 검색어 {tagged}행")
    for k, v in data.items():
        print(f"   {k:9} {len(v):4}행  검색어 {len([r for r in v if r['tags']]):4}")
    print(f"   pools     {len(pools):4}개  " + " · ".join(f"{k.split('.')[0]}:{v['n']}" for k, v in pools.items()))

    if missing:
        print(f"\n경로 오류 {len(missing)}건:")
        for m in missing[:25]:
            print("   ", m)
    if bad:
        print(f"\n후보 풀 오류 {len(bad)}건:")
        for b in bad[:25]:
            print("   ", b)
    if missing or bad:
        return 1
    print("\n검증 통과 — 참조된 파일이 전부 실재하고, 후보 풀의 섹션 이름이 전부 인덱스에 있다.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
