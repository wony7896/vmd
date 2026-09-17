#!/usr/bin/env python3
"""원고 문구를 넣으면 그 블록에 어떤 그래픽이 붙는지 보여 준다.

  python3 wiki/pick.py "5. 시즈널" "추석 명절 맞이 특가 선물 드립니다"
  python3 wiki/pick.py                       # 예시 묶음을 한꺼번에 돌린다

[template.md](template.md) 2.5 의 순위 규칙을 그대로 옮긴 참조 구현이다.
스튜디오가 자동 선택을 붙일 때 이 함수를 옮겨 쓰면 되고, 검색어를 고친 뒤
의도대로 걸리는지 확인할 때도 쓴다. 규칙이 바뀌면 문서와 여기를 함께 고친다.

  1. 원고에 검색어 낱말이 몇 개 들어 있는지 센다
     - 한 글자 검색어는 낱말 첫머리에서만 (앞이 문자열 처음이거나 공백·문장부호)
     - 두 글자 이상은 낱말 안쪽도 포함
  2. 동점이면 2.5 표에 적은 섹션 순서
  3. 그래도 동점이면 인덱스의 행 순서
  4. 한 낱말도 안 걸리면 그래픽을 비운다
"""
import json, os, re, sys, unicodedata as ud

WIKI = os.path.dirname(os.path.abspath(__file__))
N = lambda s: ud.normalize("NFC", s)
KINDS = ("icon", "illust", "product")

def load():
    return json.load(open(os.path.join(WIKI, "assets.json"), encoding="utf-8"))

# 낱말을 이루는 글자 — 한글·영문·숫자. 이 뒤에 붙은 한 글자 검색어는 낱말 속에 박힌 것이다
WORD = re.compile(r"[0-9A-Za-z\uac00-\ud7a3\u1100-\u11ff]")

def hit(tag, text):
    """원고에 검색어가 들어 있나. 한 글자는 낱말 첫머리에서만 (template.md 2.5)"""
    if len(tag) > 1:
        return tag in text
    i = text.find(tag)
    while i >= 0:
        if i == 0 or not WORD.match(text[i - 1]):
            return True
        i = text.find(tag, i + 1)
    return False

def label(r):
    f = r["fields"]
    return (f.get("한글명") or f.get("슬롯") or f.get("기종")
            or (r["section"] + " " + f.get("번호", "")).strip())

def pick(data, cat, copy):
    """(점수, 종류, 이름, 경로) 목록을 순위대로. 빈 목록이면 그래픽을 비운다"""
    pool = data["pools"].get(N(cat))
    if pool is None:
        raise SystemExit(f"블록 카테고리 '{cat}' 가 template.md 2.5 에 없다 — "
                         + " · ".join(data["pools"]))
    text, out = N(copy), []
    for kind in KINDS:
        order = pool[kind]
        for i, r in enumerate(data[kind]):
            if r["section"] not in order:
                continue
            n = sum(1 for t in r["tags"] if hit(N(t), text))
            if n:
                out.append((-n, order.index(r["section"]), i, kind, r))
    out.sort()
    return [(-s, kind, label(r), r["paths"][0]) for s, _, _, kind, r in out]

EXAMPLES = [
    ("4. 메세지 소구형", "입주 축하 통신 요금 할인 혜택 입주 박람회보다 더 좋은 상품과 가격으로"),
    ("4. 메세지 소구형", "우리 아이를 위한 키즈 요금제와 Btv 키즈"),
    ("4. 메세지 소구형", "어르신 실버 요금제 방문 설치 안내"),
    ("1. 요금 안내", "기가 인터넷 1G + B tv All+ 월 40,150원 42% 할인"),
    ("1. 요금 안내", "현금 지원 최대 30만원 페이백"),
    ("2. 사은품", "커피 기프티콘 증정 이벤트"),
    ("5. 시즈널", "추석 명절 맞이 특가 선물 드립니다"),
    ("5. 시즈널", "크리스마스 연말 이벤트 지금 가입하세요"),
    ("5. 시즈널", "여름 휴가 시원하게 물놀이 다녀오세요"),
    ("3. 요금 안내 + 상품", "갤럭시 Z 플립7 사전 예약 접수 중"),
    ("6. 서부 본부 전단", "매장으로 찾아오세요 상담 도와드립니다"),
    ("1. 요금 안내", "본사 방침에 따른 공지"),
]

def main(argv):
    data = load()
    pairs = [(argv[0], argv[1])] if len(argv) >= 2 else EXAMPLES
    if len(argv) == 1:
        raise SystemExit('사용법: python3 wiki/pick.py "블록 카테고리" "원고 문구"')
    for cat, copy in pairs:
        hits = pick(data, cat, copy)
        print(f"\n[{cat}]  후보 {data['pools'][N(cat)]['n']}개")
        print(f"  «{copy}»")
        if not hits:
            print("   걸린 검색어 없음 → 그래픽을 비운다")
            continue
        for rank, (n, kind, name, path) in enumerate(hits[:5], 1):
            mark = "→" if rank == 1 else " "
            print(f"   {mark} {n}점  {kind:7} {name:22} {os.path.basename(path)}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
