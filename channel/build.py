"""channel/src.html + channels.csv → ../channel-studio.html (브라우저로 바로 여는 단일 파일)

python3 channel/build.py          # 만들기
python3 channel/build.py --check  # 번들이 원본과 어긋나는지만 확인

channels.csv 가 데이터 원본이다. 판별 머리 날짜·가격·안내문은 아래 META 에 둔다.
서체는 studio/ 의 서브셋 woff2, 로고는 studio/logo_white.png(SK broadband 영문 화이트)를 박아 넣는다.
"""
import base64, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'channel-studio.html')

BTV_PRICES = {'미니': '7,700원', '이코노미': '9,900원', '스탠다드': '13,200원', 'All': '16,500원'}
BTV_NOTES = ['25번 OBS는 서울, 경기, 인천 지역에서만 시청할 수 있습니다.',
             "오디오 채널 301번 'B tv 뮤직'이 별도로 제공됩니다.",
             'UHD 채널은 UHD 셋톱박스로 시청 가능합니다.(셋톱박스 임대요금 별도)',
             '위 요금은 B tv 기본요금입니다.(부가세 포함, 인터넷 결합 시, 3년 약정 기준)']
POP_NOTES = ['OBS 경인TV는 방송법상의 방송권역 제한으로 서울/경기/인천지역만 시청가능합니다.',
             "오디오 채널 301번 'B tv 뮤직'이 별도로 제공됩니다."]
HSHOP = '현대홈쇼핑+shop(33번)은 중부/세종/전주/대구/대경/TCN/낙동/동남/서부산 지역에선 25번에서 시청하실 수 있습니다.'
POP_BANNER = 'B tv pop 상품 혜택 → 최신형 셋톱박스, 고화질, YouTube채널   지금 바로 신청해주세요!'

META = {
    'B tv|2023-08': dict(prices=BTV_PRICES, notes=BTV_NOTES),
    'B tv|2023-11': dict(prices=BTV_PRICES, notes=BTV_NOTES),
    'B tv|2023-12': dict(prices=BTV_PRICES, notes=BTV_NOTES, label='수정요청 적용 · 미확정'),
    'B tv pop|2023-08': dict(notes=POP_NOTES, banner=POP_BANNER),
    'B tv pop|2023-11': dict(notes=[HSHOP] + POP_NOTES, banner=POP_BANNER),
    'B tv cable|2023-11': dict(notes=[HSHOP] + POP_NOTES),
}

def data():
    v = {}
    with open(os.path.join(HERE, 'channels.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            key = f"{r['상품']}|{r['기준']}"
            y, m = r['기준'].split('-')
            d = v.setdefault(key, dict(product=r['상품'], month=r['기준'], date=f'{y}년 {int(m)}월 기준',
                                       label='', prices={}, notes=[], banner='', channels=[]))
            d['channels'].append(dict(no=int(r['번호']), name=r['채널명'], tier=r['티어'],
                                      genre=r['장르'], backName=r['뒷면표기']))
    missing = set(v) - set(META)
    if missing: sys.exit(f'META 에 없는 판: {sorted(missing)}')
    for k, m in META.items():
        if k not in v: sys.exit(f'channels.csv 에 없는 판: {k}')
        v[k].update(m)
    return v

def b64(p):
    with open(os.path.join(ROOT, p), 'rb') as f: return base64.b64encode(f.read()).decode()

def build():
    with open(os.path.join(HERE, 'src.html'), encoding='utf-8') as f: s = f.read()
    for k, val in {'{{DATA}}': json.dumps(data(), ensure_ascii=False, separators=(',', ':')),
                   '{{FONT_DISPLAY}}': b64('studio/font_display_bold.woff2'),
                   '{{FONT_TEXT}}': b64('studio/font_text_semibold.woff2'),
                   '{{LOGO}}': b64('studio/logo_white.png')}.items():
        assert k in s, k
        s = s.replace(k, val)
    return s

if __name__ == '__main__':
    out = build()
    if '--check' in sys.argv:
        cur = open(OUT, encoding='utf-8').read() if os.path.exists(OUT) else ''
        print('일치' if cur == out else '어긋남 — python3 channel/build.py 로 다시 만든다'); sys.exit(cur != out)
    with open(OUT, 'w', encoding='utf-8') as f: f.write(out)
    print(f'{OUT} ({len(out.encode()) // 1024}KB)')
