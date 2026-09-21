#!/usr/bin/env python3
"""wiki/review-checklist.md 로 검수 엣지 함수의 시스템 프롬프트를 다시 만든다.

review-checklist.md 는 원래 "검수 에이전트의 시스템 프롬프트로 그대로 붙여 넣는" 용도로
쓰여진 문서다(문서 3~4줄). 다만 문서의 7절은 사람이 읽을 마크다운 표 형식을 지시하는데,
엣지 함수는 화면에 안정적으로 그릴 수 있는 JSON이 필요하다. 그래서 이 스크립트가

    0~6절, 8절  그대로 가져오고
    7절         마크다운 표 지시를 JSON 스키마 지시로 바꿔치기

해서 하나의 프롬프트 문자열을 만들고, JSON으로 이스케이프해
studio/edge-functions/brand-review/index.ts 의 생성 구간(CHECKLIST_PROMPT)에 넣는다.

**review-checklist.md 가 원본이고 index.ts 안의 CHECKLIST_PROMPT 는 생성물이다.**
생성 구간 안을 손으로 고치지 않는다 — 체크리스트를 고쳤으면 이 스크립트를 다시 돌리고,
그 다음 Supabase MCP(deploy_edge_function)로 재배포해야 반영된다(재배포는 이 스크립트가 하지 않는다).

    python3 wiki/build-review-prompt.py          반영
    python3 wiki/build-review-prompt.py --check  차이만 보고, 쓰지 않음 (종료코드 1 = 어긋남)
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKLIST_MD = os.path.join(ROOT, 'wiki', 'review-checklist.md')
INDEX_TS = os.path.join(ROOT, 'studio', 'edge-functions', 'brand-review', 'index.ts')

SECTION_7_MARK = '## 7. 출력 형식'
SECTION_8_MARK = '## 8. 한계'

BEGIN = '// ▼▼▼ 생성 구간 — wiki/build-review-prompt.py 가 wiki/review-checklist.md 에서 만든다. 손으로 고치지 않는다. ▼▼▼\n'
END = '// ▲▲▲ 생성 구간 끝 ▲▲▲\n'

JSON_SECTION_7 = """## 7. 출력 형식 (JSON 전용)

마크다운 표나 다른 설명 없이, 아래 스키마 그대로 **JSON 객체 하나만** 출력한다.
코드펜스(```)도 쓰지 않는다 — 첫 글자가 `{`, 마지막 글자가 `}` 여야 한다.

{
  "items": [
    {"key": "color",   "verdict": "pass|fail|warn",      "found": "...", "rule": "...", "fix": "..."},
    {"key": "logo",    "verdict": "pass|fail|warn|na",    "found": "...", "rule": "...", "fix": "..."},
    {"key": "typo",    "verdict": "pass|fail|warn|na",    "found": "...", "rule": "...", "fix": "..."},
    {"key": "graphic", "verdict": "pass|fail|warn|na",    "found": "...", "rule": "...", "fix": "..."},
    {"key": "tone",    "verdict": "tone_ok|tone_soft|tone_off", "found": "..."},
    {"key": "grid",    "verdict": "pass|fail|na",         "found": "...", "rule": "...", "fix": "..."}
  ],
  "overall": "publishable|bx_review|fix_needed",
  "overall_note": "..."
}

- `items` 는 이 순서·이 6개 key 를 모두 포함한다. 빠뜨리지 않는다.
- `verdict` 의 "대상 아님"은 `"na"`, 5절의 "부합"은 `"tone_ok"`, "다소 어긋남"은 `"tone_soft"`,
  "명확히 이질적"은 `"tone_off"` 로 옮긴다.
- `found` / `rule` / `fix` 는 전부 문자열이다. 해당 없으면 빈 문자열 `""`로 둔다.
- `overall` 은 1~6절 판정을 종합해 정한다: 명백한 위반이 하나라도 있으면 `fix_needed`,
  위반은 없지만 확인 필요·제휴 로고 등 경미한 항목이 있으면 `bx_review`, 위반이 전혀 없으면
  `publishable`.

**`warn`("확인 필요")을 아무 때나 쓰는 안전판으로 삼지 않는다.** 아래를 반드시 지킨다.

- **verdict은 found·fix에 스스로 적은 판단과 일치해야 한다.** found나 fix에 "위반으로 보인다" ·
  "규정에 어긋난다"라고 적어 놓고 verdict을 warn으로 낮추지 않는다 — 그렇게 판단했으면 `fail`이다.
  반대로 별다른 근거 없이 verdict만 warn으로 두지 않는다.
- `warn`은 다음 두 경우에만 쓴다: (1) 이미지 한 장으로는 근본적으로 실측이 불가능한 항목(로고
  여백·크기의 mm 값, 그리드 마진의 mm 값), (2) 색상·서체가 육안으로 구분 안 갈 만큼 미세하게
  근접한 경우. "100% 확신할 수 없다"는 것 자체는 이유가 아니다 — 이미지에서 관찰되는 증거로
  판단이 서면 pass 또는 fail로 정한다.
- **로고 여백·크기(2.3)·그리드 마진처럼 mm 실측이 불가능한 항목**도 이미지 안에서의 상대적
  비율로 pass/fail을 정하고, found에 "정확한 mm 실측은 원본 파일 필요"라는 caveat만 덧붙인다.
  이 caveat이 있다고 verdict을 자동으로 warn으로 낮추지 않는다.
- **타이포그래피(3.1)**: "SKT Sans로 보임"이면 `pass`, "다른 서체로 보임"이면 `fail`이다. 서체를
  100% 확정할 수 없다는 사실 자체는 warn 사유가 아니다 — 골격이 브랜드 서체와 가까우면 pass,
  명백히 다르면(손글씨체·세리프체 등) fail로 정한다.
- **그래픽·비주얼 에셋(4절)**: 워터마크·가이드와 확연히 다른 렌더링 방식 등 외부 소스라는 구체적
  증거가 있을 때만 위반이다. 그런 증거가 없으면 "완전히 배제할 수 없다"는 이유만으로 warn을
  쓰지 않고 pass로 정한다.
"""


def build_prompt():
    with open(CHECKLIST_MD, 'r', encoding='utf-8') as f:
        text = f.read()
    i7 = text.index(SECTION_7_MARK)
    i8 = text.index(SECTION_8_MARK)
    if not (i7 < i8):
        sys.exit('review-checklist.md 구조가 바뀌었다 — 7절/8절 위치를 확인해라')
    before = text[:i7]
    after = text[i8:]
    return before + JSON_SECTION_7 + '\n---\n\n' + after


def render_block(prompt):
    literal = json.dumps(prompt, ensure_ascii=False)
    return BEGIN + 'const CHECKLIST_PROMPT = ' + literal + ';\n' + END


def main():
    check_only = '--check' in sys.argv[1:]
    prompt = build_prompt()
    new_block = render_block(prompt)

    with open(INDEX_TS, 'r', encoding='utf-8') as f:
        ts = f.read()
    if BEGIN not in ts or END not in ts:
        sys.exit('index.ts 에서 생성 구간 마커를 찾지 못했다')
    start = ts.index(BEGIN)
    stop = ts.index(END) + len(END)
    old_block = ts[start:stop]

    if old_block == new_block:
        print('일치 — CHECKLIST_PROMPT 가 이미 review-checklist.md 최신본과 같다')
        return 0

    if check_only:
        print('어긋남 — review-checklist.md 가 바뀌었는데 index.ts 의 CHECKLIST_PROMPT 가 예전 것이다')
        print('  python3 wiki/build-review-prompt.py 로 반영해라')
        return 1

    new_ts = ts[:start] + new_block + ts[stop:]
    with open(INDEX_TS, 'w', encoding='utf-8') as f:
        f.write(new_ts)
    print('반영: CHECKLIST_PROMPT (%d자)' % len(prompt))
    print('다음: Supabase MCP deploy_edge_function 으로 brand-review 를 재배포해야 실제 반영된다')
    return 0


if __name__ == '__main__':
    sys.exit(main())
