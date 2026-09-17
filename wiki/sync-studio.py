#!/usr/bin/env python3
"""studio/ 원본을 flyer-studio.html 번들에 반영한다.

전단지 스튜디오는 같은 내용을 두 곳에 들고 있다.

    studio/Main.dc.html · Flyer.dc.html · canvas.json   ← 원본. 여기를 고친다
    flyer-studio.html   <script id="appifact-doc">      ← 배포 번들. 생성물

두 사본은 이미지 참조 방식만 다르다. 원본은 `../brand guide/...` 실제 경로를 쓰고,
번들은 에셋을 평평한 이름으로 품고 있다. 이 스크립트가 그 차이만 바꿔 끼운다.

**md·dc.html 이 원본이고 번들은 생성물이다.** 번들 안 JSON 을 직접 고치지 않는다.

    python3 wiki/sync-studio.py          반영
    python3 wiki/sync-studio.py --check  차이만 보고, 쓰지 않음 (종료코드 1 = 어긋남)
"""

import base64
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.path.join(ROOT, 'flyer-studio.html')
OPEN_TAG = '<script type="application/json" id="appifact-doc">'
SOURCES = ('Main.dc.html', 'Flyer.dc.html', 'canvas.json')

# studio/ 의 실제 경로 -> 번들 안 평평한 에셋 이름
PATHMAP = (
    ('../brand guide/logo/SK broadband_logo_black_영문_인쇄용.png', 'logo_black.png'),
    ('../brand guide/logo/SK broadband_logo_white_영문_인쇄용.png', 'logo_white.png'),
    ('../brand guide/logo/B_logo_black_인쇄용.png', 'B_logo_black.png'),
)


# 서브셋 웹폰트 — wiki/subset-font.py 가 만든다
FONTS = ('font_display_bold.woff2', 'font_text_semibold.woff2')


def flatten(text):
    for real, flat in PATHMAP:
        text = text.replace(real, flat)
    return text


def inline_fonts(text):
    """@font-face 의 url() 을 data: URI 로 바꿔 넣는다.

    아트보드 런타임은 `src="이름"` 과 `url(이름)` 을 **글자 그대로 찾아** 번들 에셋의
    data: URI 로 바꿔 주는데, **이미지 확장자만** 그렇게 한다 (png·jpg·gif·webp·avif·bmp·svg).
    woff2 는 대상이 아니라 그대로 남고, 아트보드는 격리된 프레임이라 네트워크로도 못 받는다.
    그래서 폰트만 여기서 CSS 안에 통째로 박아 넣는다 — 그래픽은 런타임이 알아서 바꿔 준다.

    studio/ 원본은 상대경로를 그대로 둔다 — 캔버스 편집기가 디스크에서 열 때는 그게 맞다.
    """
    for name in FONTS:
        ref = 'url("%s")' % name
        if ref not in text:
            continue
        path = os.path.join(ROOT, 'studio', name)
        if not os.path.exists(path):
            sys.exit('서브셋 폰트가 없다: studio/%s\n'
                     '  python3 wiki/subset-font.py 로 만든다' % name)
        b64 = base64.b64encode(open(path, 'rb').read()).decode('ascii')
        text = text.replace(ref, 'url("data:font/woff2;base64,%s")' % b64)
    return text


def load_bundle():
    s = open(BUNDLE, encoding='utf-8').read()
    try:
        i = s.index(OPEN_TAG) + len(OPEN_TAG)
        j = s.index('</script>', i)
    except ValueError:
        sys.exit('flyer-studio.html 에서 appifact-doc 블록을 찾지 못했다')
    return s, i, j, json.loads(s[i:j])


def studio_default_text(main_html):
    """Main.dc.html 초기 state 에 박힌 사용자 문구를 뽑는다."""
    body = main_html
    head = body.find('chosen: [')
    tail = body.find('nextUid:', head)
    if head < 0 or tail < 0:
        return []
    block = body[head:tail] + body[tail:body.find('}', body.find('f: {', tail)) + 1]
    out = []
    keys = ('headline', 'sub', 'product', 'list', 'price', 'rate', 'note', 'store', 'phone')
    for key in keys:
        for m in re.finditer(r"\b%s:\s*'((?:[^'\\]|\\.)*)'" % key, block):
            raw = m.group(1).replace("\\n", "\n").replace("\\'", "'")
            for line in raw.split("\n"):
                line = line.strip()
                if line and line not in out:
                    out.append(line)
    return out


def visible_text(html):
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', html, flags=re.S | re.I)
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.I)
    t = re.sub(r'<!--.*?-->', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'[ \t]+', ' ', t)


def content_drift(files):
    """결과물 견본이 스튜디오 기본 문서와 같은 문구를 쓰는지."""
    wanted = studio_default_text(files['Main.dc.html'])
    have = visible_text(files['Flyer.dc.html'])
    return [w for w in wanted if w not in have]


def main():
    check_only = '--check' in sys.argv
    s, i, j, doc = load_bundle()
    files = doc['content']['files']

    changed = []
    for name in SOURCES:
        path = os.path.join(ROOT, 'studio', name)
        if not os.path.exists(path):
            sys.exit('원본이 없다: studio/%s' % name)
        new = inline_fonts(flatten(open(path, encoding='utf-8').read()))
        if '../brand guide/' in new:
            left = sorted(set(re.findall(r'\.\./brand guide/[^"\']+', new)))
            sys.exit('PATHMAP 에 없는 에셋 경로: %s\n  wiki/sync-studio.py 의 PATHMAP 에 추가하고 번들에도 파일을 넣어라' % left)
        if files.get(name) != new:
            files[name] = new
            changed.append(name)

    # 마크업이 참조하는 에셋을 studio/ 에서 번들로 (번들은 base64 로 품는다)
    # url("...") 도 함께 모은다 — 그래픽 후보는 CSS 변수로 들어오므로 src 가 아니다.
    # 런타임은 이미지 확장자에 한해 src="이름" 과 url(이름) 을 둘 다 data: URI 로 바꿔 준다
    # (woff2 는 안 바꿔 줘서 inline_fonts 가 따로 박아 넣는다).
    refs = set()
    for name in ('Main.dc.html', 'Flyer.dc.html'):
        refs |= set(re.findall(r'src="([^"\'{}]+)"', files[name]))
        refs |= set(re.findall(r'url\("([^"\'{}]+\.(?:png|jpe?g|gif|webp|avif|bmp|svg))"\)', files[name]))
        refs |= set(re.findall(r"assetSrc'?: *'([^']+\.png)'", files[name]))
        refs |= set(re.findall(r"file: '([^']+\.png)'", files[name]))
    refs.discard('./support.js')
    # 평평한 이름은 PATHMAP 의 원본에서 읽는다 (studio/ 의 동명 파일이 아니라)
    flat_src = {flat: os.path.join(ROOT, 'studio', real) for real, flat in PATHMAP}
    missing = []
    for ref in sorted(refs):
        local = flat_src.get(ref) or os.path.join(ROOT, 'studio', ref)
        if os.path.exists(local):
            enc = base64.b64encode(open(local, 'rb').read()).decode('ascii')
            if files.get(ref) != enc:
                files[ref] = enc
                changed.append(ref)
        elif ref not in files:
            missing.append(ref)
    if missing:
        sys.exit('studio/ 에도 번들에도 없는 에셋을 참조한다: %s' % missing)

    for name in FONTS:
        if files.pop(name, None) is not None:
            changed.append(name + ' (CSS 안으로 옮김)')

    # 아무도 안 쓰는 에셋은 번들에서 뺀다. 번들은 생성물이라 남겨 둘 이유가 없고,
    # 그래픽이 190개로 늘면서 유령 하나가 곧 용량이다
    orphan = sorted(k for k in files
                    if k.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif', '.svg'))
                    and k not in refs)
    for k in orphan:
        del files[k]
        changed.append(k + ' (참조 없음 — 뺌)')

    drift = content_drift(files)
    if drift:
        print('견본이 스튜디오 기본 문서와 어긋난다 — Flyer.dc.html 에 없는 문구:')
        for line in drift:
            print('  · %s' % line)
        if not check_only:
            print('  (번들은 반영했다. 위 문구를 Flyer.dc.html 에 맞춰 넣어라)')

    if check_only:
        if changed:
            print('어긋남: %s' % ', '.join(changed))
            return 1
        print('일치 — 번들이 studio/ 원본과 같다')
        return 0

    if not changed:
        print('변경 없음 — 번들이 이미 최신이다')
        return 0

    # 원본과 같은 인코딩: 압축 JSON + '<' 를 < 로 이스케이프해 script 조기 종료를 막는다
    out = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    assert '</script>' not in out
    open(BUNDLE, 'w', encoding='utf-8').write(s[:i] + '\n' + out + '\n' + s[j:])
    print('반영: %s' % ', '.join(changed))
    print('에셋 참조 %d개 모두 번들에 있음' % len(refs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
