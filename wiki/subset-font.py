#!/usr/bin/env python3
"""전단지 도구가 품고 다닐 SKT Sans 서브셋 2종을 만든다.

    python3 wiki/subset-font.py

원본 웹폰트는 한 벌에 470KB 다 — 11,172 한글 음절을 전부 들고 있기 때문이다.
전단지 원고는 그 파일을 통째로 품고 나가야 하므로(아트보드가 격리된 프레임이라
네트워크로 못 받는다) **KS X 1001 완성형 2,350자**로 잘라 130KB 대로 줄인다.

    brand guide/font/web/SKTSansDisplay-Bold.woff2    → studio/font_display_bold.woff2
    brand guide/font/web/SKTSansText-SemiBold.woff2   → studio/font_text_semibold.woff2

**두 벌만 쓴다.** wiki/template.md 3 의 본문 규정이 제목=제목체 Bold ·
본문=본문체 SemiBold 이고, 전단지가 실제로 쓰는 웨이트가 그 둘뿐이다.

KS X 1001 밖의 음절(뷁·똠 같은 확장 완성형)은 빠진다. 그런 글자를 쓰면 그 글자만
시스템 서체로 떨어진다. 전단지 카피에 쓸 일이 없어 이 선을 골랐다.

fonttools 가 필요하다. 없으면 설치 방법을 알려 주고 멈춘다.
**원본이 brand guide/ 이고 studio/ 의 woff2 는 생성물이다.** 직접 고치지 않는다.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "brand guide", "font", "web")
OUT = os.path.join(ROOT, "studio")

FACES = (
    ("SKTSansDisplay-Bold.woff2", "font_display_bold.woff2", "제목체 Bold"),
    ("SKTSansText-SemiBold.woff2", "font_text_semibold.woff2", "본문체 SemiBold"),
)

# 한글 밖에서 남길 것 — 라틴·구두점·원화·괄호·원문자·기호
UNICODES = (
    "U+0020-007E,U+00A0-00FF,U+2010-206F,U+20A9,U+20AC,U+2122,"
    "U+2460-2473,U+25A0-25CF,U+3000-303F,U+3131-3163,U+FF01-FF60"
)


def ksx1001():
    """KS X 1001 완성형 2,350자 — EUC-KR 두 바이트가 모두 0xA1~0xFE 인 음절.

    파이썬의 euc_kr 코덱은 CP949(확장 완성형 11,172자)까지 받아 주므로
    바이트 범위로 한 번 더 거른다. 이게 없으면 전부 통과해 서브셋이 안 된다.
    """
    out = []
    for c in range(0xAC00, 0xD7A4):
        try:
            b = chr(c).encode("euc-kr")
        except UnicodeEncodeError:
            continue
        if len(b) == 2 and 0xA1 <= b[0] <= 0xFE and 0xA1 <= b[1] <= 0xFE:
            out.append(chr(c))
    return "".join(out)


def main():
    try:
        from fontTools import subset
    except ImportError:
        print("fonttools 가 없다. 서브셋을 만들려면 먼저 설치한다:\n")
        print("    python3 -m venv .venv && .venv/bin/pip install fonttools brotli")
        print("    .venv/bin/python wiki/subset-font.py\n")
        print("이미 만들어 둔 studio/font_*.woff2 가 있으면 그대로 써도 된다.")
        return 1

    text = ksx1001()
    print("KS X 1001 한글 음절 %d자" % len(text))

    for src, dst, label in FACES:
        sp = os.path.join(SRC, src)
        dp = os.path.join(OUT, dst)
        if not os.path.exists(sp):
            print("  ! 원본이 없다: %s" % sp)
            return 1
        args = [sp, "--output-file=" + dp, "--flavor=woff2",
                "--text=" + text, "--unicodes=" + UNICODES,
                "--layout-features=*", "--no-hinting", "--desubroutinize"]
        subset.main(args)
        before = os.path.getsize(sp) / 1024
        after = os.path.getsize(dp) / 1024
        print("  %-16s %6.1f KB → %6.1f KB  (%.0f%%)  %s"
              % (label, before, after, after / before * 100, dst))

    print("\nstudio/ 에 넣었다. 번들에 반영하려면 python3 wiki/sync-studio.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
