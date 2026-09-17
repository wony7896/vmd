# SK브로드밴드 소매 매장 전단지 — 작업 규칙

A5(148×210mm) 전단지를 브랜드 규정에 맞게 제작한다.
브랜드 규칙과 사용 가능한 에셋은 전부 `wiki/`에 있다.

## 라우팅 — 무엇을 할 때 무엇을 읽는가

| 필요한 것 | 읽을 문서 |
|---|---|
| **지금 어디까지 왔나 · 남은 일** (처음 이어받을 때) | [이어받기.md](이어받기.md) |
| 컬러 HEX · 배경별 조합 · 서체 규정 · 그리드 | [wiki/brand.md](wiki/brand.md) |
| 로고 파일 고르기 · 크기 · 여백 | [wiki/assets-logo.md](wiki/assets-logo.md) |
| 블록 조합 · 판형 · 레이아웃 제약 | [wiki/template.md](wiki/template.md) |
| 어느 블록에 어떤 그래픽이 올 수 있나 | [wiki/template.md](wiki/template.md) 2.5 |
| 아이콘 고르기 | [wiki/assets-icon.md](wiki/assets-icon.md) |
| 인물 일러스트 고르기 | [wiki/assets-illust.md](wiki/assets-illust.md) |
| 단말기 사진 | [wiki/assets-product.md](wiki/assets-product.md) |
| 라인 아이콘 · 2D 아이콘 | [wiki/assets-line-icon.md](wiki/assets-line-icon.md) |
| 서체 · `@font-face` · 웹폰트 · 서브셋 | [wiki/typography.md](wiki/typography.md) |
| 코드에서 에셋 목록이 필요할 때 | `wiki/assets.json` |

**색·로고·서체는 한 문서(brand.md)에 함께 있다.** 배경색 하나가 배지 색·로고 버전·
텍스트 하이라이트를 연쇄로 결정하기 때문이다. 색만 읽고 로고를 고르지 않는다.

## 금지

- **위키에 등재되지 않은 이미지 파일을 쓰지 않는다.** `brand guide/` 폴더를 직접 뒤지지 않는다.
- 각 인덱스의 "목록 외" 절에 있는 파일을 쓰지 않는다. BX팀 미확인 자산이다.
- brand.md에 없는 컬러 값을 만들어내지 않는다 (1.7 Color Don'ts).
- "결번"으로 표시된 항목을 선택지로 제시하지 않는다. 파일이 없다.

## 에셋을 고르는 순서

1. 블록에 넣을 그래픽이면 **후보 범위부터 좁힌다.** [wiki/template.md](wiki/template.md) 2.5가
   블록 카테고리마다 고를 수 있는 섹션을 한정한다. 아이콘 141개 전체에서 고르지 않는다.
2. 그 안에서 **검색어** 열로 찾는다. 파일명·영문 슬롯으로 찾지 않는다.
   원고 문구와 겹치는 낱말이 많은 것이 앞선다. 인물 일러스트는 섹션 머리의 `> 검색어:` 줄을 본다.
3. **정본** 열의 파일을 쓴다. `_STD`(1400×1400)가 정본이다.
4. 대형 인쇄물(X배너·플래카드·A2 이상)일 때만 **고해상** 열을 쓴다.
5. 배경 위 사용 규정은 brand.md 1.6을 확인한다.

맞는 후보가 없으면 **그래픽을 비운다.** 어울리지 않는 그림을 넣는 것보다 낫다.

## 위키를 수정했을 때

```bash
python3 wiki/build.py
```

`wiki/*.md`의 표를 읽어 `wiki/assets.json`을 다시 만든다. 두 가지를 검증하고, 어느 쪽이든
어긋나면 **빌드가 실패한다.**

- 참조된 파일이 실재하는지
- `template.md` 2.5 후보 풀에 적힌 섹션 이름이 인덱스에 있는지

에셋마다 `검색어`(`tags`)와 블록 카테고리별 후보 풀(`pools`)이 함께 실려 나간다.
**md가 원본이고 json은 생성물이다.** json을 직접 고치지 않는다.

## 검색어를 고쳤을 때 — 어떤 그래픽이 붙는지 확인

```bash
python3 wiki/pick.py "5. 시즈널" "추석 명절 맞이 특가 선물 드립니다"
```

원고 문구를 넣으면 그 블록에 붙을 그래픽을 순위대로 보여 준다. 인자 없이 돌리면 예시 묶음을 한꺼번에 돌린다.
[wiki/template.md](wiki/template.md) 2.5 순위 규칙의 **참조 구현**이고, 스튜디오의 `gfxRank()`가
같은 규칙을 JS로 옮긴 것이다. 터미널 결과와 도구 화면이 어긋나면 둘 중 하나가 규칙에서 샌 것이다.
**규칙을 바꿀 때는 문서 · `pick.py` · `Main.dc.html` 의 `gfxRank()` 셋을 함께 고친다.**

## 그래픽 후보를 다시 만들 때

```bash
python3 wiki/build-graphics.py
```

후보 풀(`assets.json` 의 `pools`)에 드는 원본 **190개를 긴 변 160px 로 줄여** `studio/asset/` 에 넣고,
`studio/Main.dc.html` 의 **생성 구간 두 곳**(CSS 변수 · 카탈로그)을 다시 쓴다.
검색어나 후보 풀을 고친 뒤 `build.py` 다음에 돌린다. `--check` 를 붙이면 어긋난 것만 알려준다.
크기는 스크립트 머리의 `PX` 하나가 정한다 — 바꾸면 `studio/asset/size.txt` 가 어긋나 190장을 전부 다시 만든다.
번들 용량이 여기서 나온다 (160px → 6.8MB · 220px → 9.6MB).

> **그림은 CSS 변수로만 들어간다.** 아트보드 런타임은 `src="이름.png"` 와 `url(이름.png)` 를
> 글자 그대로 찾아 바꿔 주지만 `src="{{변수}}"` 는 바꿔 주지 않는다(직접 시험해 확인).
> 그래서 190개를 `--g-g001` 같은 변수로 미리 박아 두고 코드는 변수 이름만 고른다.
> **생성 구간 안을 손으로 고치지 않는다.**

## 스튜디오를 수정했을 때

```bash
python3 wiki/sync-studio.py
```

`studio/Main.dc.html` · `Flyer.dc.html` · `canvas.json`을 배포 번들 `flyer-studio.html`
안의 `appifact-doc` 블록에 반영한다. 두 사본은 에셋 참조 방식만 다르고(원본은
`../brand guide/...`와 상대경로, 번들은 평평한 이름과 `data:` URI) 스크립트가 그 차이를
바꿔 끼운다. 런타임은 `src="이름"`과 `url(이름)`을 **이미지 확장자에 한해** 풀어 주므로,
그래픽은 맡겨 두고 **웹폰트(woff2)만** 스크립트가 base64로 박아 넣는다.
**studio/가 원본이고 번들은 생성물이다.** 번들 안 JSON을 직접 고치지 않는다.
`--check`를 붙이면 쓰지 않고 어긋난 파일만 알려준다.
참조되지 않는 번들 에셋은 빼 준다 — 그래픽이 190개라 유령 하나가 곧 용량이다.

## 서체 서브셋을 다시 만들 때

```bash
python3 wiki/subset-font.py
```

`brand guide/font/web/`의 원본 2종을 KS X 1001 2,350자로 잘라 `studio/font_*.woff2`로
넣는다(467KB → 132KB). 원고는 폰트를 파일 안에 품고 나가야 해서 필요하다.
fonttools가 있어야 하고, 없으면 설치 방법을 알려주고 멈춘다.
**brand guide/가 원본이고 studio/의 woff2는 생성물이다.**
만든 뒤에는 `sync-studio.py`를 돌려 번들에 반영한다.

## 주의 — 한글 파일명 인코딩

macOS는 한글 파일명을 **NFD(자모 분리)** 로 저장하는데 위키 문서는 NFC로 적혀 있다.
`grep`·`find`·문자열 비교가 한글 파일을 못 찾는다. 파일명을 다룰 때는 반드시 정규화한다.

```python
import unicodedata as ud
ud.normalize("NFC", filename)
```

## 폴더

```
brand guide/
├── 3D Icon/              169  아이콘 — assets-icon.md
├── 3D Illustration/       66  인물 — assets-illust.md
├── Product Photography/   22  단말기 — assets-product.md
├── Line Icon/png/        210  라인 아이콘 추출본 — assets-line-icon.md
├── 2D Icon/png/           10  2D 아이콘 추출본 — assets-line-icon.md
├── logo/                   6  CI 6종 — assets-logo.md (BI 없음)
└── font/                  12  OTF 원본 + web/ WOFF2 12 — typography.md
template/                      원본 가이드 PDF
studio/  flyer-studio.html     제작 도구
studio/asset/            190  후보 그래픽 160px 축소본 — build-graphics.py 생성물
대조결과.md                     공식 목록 대조 기록 · 미결 항목
이어받기.md                     진행 상황 · 남은 일 · 되짚을 판단
```
