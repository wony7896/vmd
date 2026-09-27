"""채널표 원본 → channels.csv / 변경내역.md
python3 src/build.py   (pymupdf 필요)
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from extract import run
import nov_transcribed as T

ROOT = '/mnt/project-files/채널표'
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUNK = ('개 전 채널', )

def clean(front):
    return {n: [e for e in v if not any(j in e[1] for j in JUNK) and e[1] not in ('원', ',')] for n, v in front.items()}

def from_pdf(path, tiers):
    f, b, heads, gh = run(path, tiers)
    f = clean(f)
    ch = {}
    for n, v in f.items():
        if v: ch[n] = dict(번호=n, 채널명=v[0][1], 티어=v[0][0], 장르='', 뒷면표기='')
    for n, v in b.items():
        g, name, _ = v[0]
        if n in ch:
            ch[n]['장르'] = g
            if name.replace(' ', '').lower() != ch[n]['채널명'].replace(' ', '').lower(): ch[n]['뒷면표기'] = name
        else:
            ch[n] = dict(번호=n, 채널명=name, 티어='유료(별도)' if g == '유료채널' else '', 장르=g, 뒷면표기='')
    return ch, [int(h) for h in heads]

def split(s): return [(int(a.split(' ', 1)[0]), a.split(' ', 1)[1]) for a in s.split('|')]

def pop_nov():
    genre = {int(n): g for g, ns in T.GENRES.items() for n in ns.split()}
    ch = {}
    for tier, s in T.POP_FRONT.items():
        for n, name in split(s): ch[n] = dict(번호=n, 채널명=name, 티어=tier, 장르=genre.get(n, ''), 뒷면표기='')
    for n, name in split(T.PAID): ch[n] = dict(번호=n, 채널명=name, 티어='유료(별도)', 장르='유료채널', 뒷면표기='')
    assert not set(genre) - set(ch), set(genre) - set(ch)
    return ch

def cable_nov(pop):
    ch = {}
    for tier, s in T.CABLE_FRONT.items():
        for n in map(int, s.split()):
            c = dict(pop[n]); c['티어'] = tier
            if n == 999: c['채널명'] = '홈초이스'
            ch[n] = c
    for n, c in pop.items():
        if c['티어'] == '유료(별도)': ch[n] = dict(c)
    return ch

def btv_nov(aug):
    ch = {n: dict(c) for n, c in aug.items()}
    ch[188]['티어'] = '미니'
    for n in (270, 190): del ch[n]
    ch[273].update(채널명='Smithsonian Channel', 티어='스탠다드')
    ch[228].update(채널명='MAXPORTS', 장르='스포츠')
    ch[292].update(채널명='CGN', 뒷면표기='')
    return ch

DEC_RENUMBER = [(24, 29), (29, 31), (31, 33), (33, 2), (35, 37), (37, 39), (39, 35),
                (40, 24), (969, 972), (971, 968), (972, 967), (232, 971), (228, 969)]
def btv_dec(nov):
    ch = {n: dict(c) for n, c in nov.items()}
    for n in (161, 191, 278): del ch[n]
    moved = {new: dict(ch[old], 번호=new) for old, new in DEC_RENUMBER}
    for old, _ in DEC_RENUMBER: del ch[old]
    assert not set(moved) & set(ch), set(moved) & set(ch)
    ch.update(moved)
    ch[969]['티어'] = '이코노미'          # MAXPORTS All → 이코노미
    ch[971]['장르'] = '스포츠'            # 스크린골프존 취미/레저 → 스포츠
    return ch

TIERS = {'B tv': ['미니', '이코노미', '스탠다드', 'All'],
         'B tv pop': ['pop 100', 'pop 180', 'pop 230'],
         'B tv cable': ['cable 100', 'cable 190', 'cable 200']}

def front_key(prod, n):   # 앞면 나열 순서: B tv는 9xx가 먼저, pop·cable은 번호순
    return (0 if n >= 900 else 1, n) if prod == 'B tv' else (0, n)

def counts(prod, ch):
    r, acc = [], 0
    for t in TIERS[prod]:
        acc += sum(1 for c in ch.values() if c['티어'] == t); r.append(acc)
    return r

def main():
    btv_aug, h1 = from_pdf(f'{ROOT}/230726_B tv 채널표/업로드용/230726_B tv 채널표.pdf', TIERS['B tv'])
    pop_aug, h2 = from_pdf(f'{ROOT}/230726_B tv pop 채널표/업로드용/230726_B tv pop_채널표.pdf', TIERS['B tv pop'])
    pn = pop_nov(); cn = cable_nov(pn); bn = btv_nov(btv_aug); bd = btv_dec(bn)
    sets = [('B tv', '2023-08', btv_aug, '230726 PDF', h1),
            ('B tv', '2023-11', bn, '12월 수정요청 pptx 속 11월판 이미지', [59, 182, 233, 259]),
            ('B tv', '2023-12', bd, '11월판 + 12월 수정요청 적용 (미확정)', [60, 183, 232, 256]),
            ('B tv pop', '2023-08', pop_aug, '230726 PDF', h2),
            ('B tv pop', '2023-11', pn, '231108 .ai', list(T.POP_COUNTS.values())),
            ('B tv cable', '2023-11', cn, '231108 .ai', list(T.CABLE_COUNTS.values()))]
    rows, report = [], []
    for prod, ver, ch, src, stated in sets:
        got = counts(prod, ch)
        report.append((prod, ver, src, got, stated))
        tier_i = {t: i for i, t in enumerate(TIERS[prod])}
        for c in sorted(ch.values(), key=lambda c: (tier_i.get(c['티어'], 99), front_key(prod, c['번호']))):
            rows.append(dict(상품=prod, 기준=ver, **c))
    with open(f'{OUT}/channels.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['상품', '기준', '티어', '번호', '채널명', '장르', '뒷면표기'])
        w.writeheader(); w.writerows(rows)
    for r in report: print(*r)
    return sets, report

if __name__ == '__main__': main()
