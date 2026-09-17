# 타이포그래피 — SKT Sans

> 원본: `../brand guide/font/` OTF 12종 · 웹폰트: `../brand guide/font/web/` WOFF2 12종
> 규정: [brand.md](brand.md) 3. 타이포그래피 (4.1 ~ 4.5)
> 갱신 2026-09-15

## 서체 체계

| 서체 | CSS 패밀리 | 용도 |
|---|---|---|
| SKT Sans 제목체 | `SKT Sans Display` | 제목·헤드라인 |
| SKT Sans 본문체 | `SKT Sans Text` | 본문·캡션 |
| SKT Sans 점자 | `SKT Sans Braille` | 점자 — 별도 패밀리로 분리 |

전용 서체를 **우선 사용**한다. 다른 서체가 필요하면 유관부서 협의(brand.md 3.1).
웹 전단지 도구는 **폰트 교체 UI를 제공하지 않는다.**

## 웨이트

| 웨이트 | CSS `font-weight` | 제목체 | 본문체 |
|---|---|---|---|
| ExtraLight | `300` | ✅ | — |
| Light | `350` | ✅ | ✅ |
| Regular | `400` | ✅ | ✅ |
| SemiBold | `600` | **결번** | ✅ |
| Bold | `700` | ✅ | ✅ |
| ExtraBold | `800` | ✅ | ✅ |

> **제목체 SemiBold가 없다 — BX 확인 완료(2026-09-17), 원본 자체가 없다.** brand.md 3.1은
> 제목체 웨이트로 SemiBold를 규정하지만 대응하는 폰트 파일이 애초에 제작되지 않았다.
> 더 요청할 원본이 없으므로 **영구히 Regular(400) 또는 Bold(700)로 대체한다.**

> `Light`는 일반적인 300이 아니라 **350**이다(폰트 파일의 `usWeightClass` 값). `font-weight: 300`으로
> 지정하면 ExtraLight가 잡힌다. 표의 값을 그대로 쓴다.

## 함정 두 가지

**1. 원본 OTF는 웨이트마다 패밀리명이 다르다.**
`SKTSans제목체-Bold.otf`의 패밀리명은 `SKT Sans Display`가 아니라 **`SKT Sans Display Bold`** 다.
그래서 OTF를 그대로 쓰면 `font-family: "SKT Sans Display"; font-weight: 700`이 동작하지 않는다.
아래 `@font-face`가 12개 파일을 **3개 패밀리로 묶어** 이 문제를 해결한다. 반드시 이 선언을 쓴다.

**2. 점자체가 `usWeightClass: 900`으로 들어 있다.**
점자체를 본문 패밀리에 합치면 `font-weight: 900`에서 **점자가 렌더링된다.**
그래서 `SKT Sans Braille`로 패밀리를 분리했다. 본문·제목 패밀리에 절대 합치지 않는다.

## @font-face — 이대로 복사해 쓴다

```css
/* SKT Sans Display — 제목체 */
@font-face { font-family:"SKT Sans Display"; font-weight:300; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansDisplay-ExtraLight.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Display"; font-weight:350; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansDisplay-Light.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Display"; font-weight:400; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansDisplay-Regular.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Display"; font-weight:700; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansDisplay-Bold.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Display"; font-weight:800; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansDisplay-ExtraBold.woff2") format("woff2"); }

/* SKT Sans Text — 본문체 */
@font-face { font-family:"SKT Sans Text"; font-weight:350; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansText-Light.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Text"; font-weight:400; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansText-Regular.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Text"; font-weight:600; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansText-SemiBold.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Text"; font-weight:700; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansText-Bold.woff2") format("woff2"); }
@font-face { font-family:"SKT Sans Text"; font-weight:800; font-style:normal; font-display:swap;
  src:url("../brand guide/font/web/SKTSansText-ExtraBold.woff2") format("woff2"); }

/* SKT Sans Braille — 점자. 본문/제목 패밀리에 합치지 않는다 */
@font-face { font-family:"SKT Sans Braille"; font-weight:400; font-style:normal;
  src:url("../brand guide/font/web/SKTSansDisplay-Braille.woff2") format("woff2"); }

:root {
  --font-display: "SKT Sans Display", -apple-system, "Apple SD Gothic Neo", sans-serif;
  --font-text:    "SKT Sans Text",    -apple-system, "Apple SD Gothic Neo", sans-serif;
}
```

> 경로는 문서 기준(`wiki/`)이다. HTML에서 쓸 때는 그 파일 위치에 맞게 고친다.
> 예: 프로젝트 루트의 flyer-studio.html 이면 `../` 를 뺀 형태, 즉 프로젝트 루트 기준 “brand guide” 폴더부터 시작한다.

## 검증

`wiki/_font-test.html` 을 로컬 서버로 열면 위 `@font-face`가 실제로 로드되는지 확인할 수 있다.
페이지 하단에 `document.fonts.check()` 결과가 표시된다. 2026-09-15 확인: **Display 3/3, Text 2/2 로드 성공.**

## 파일 목록

| WOFF2 | 원본 OTF | 크기 |
|---|---|---|
| `../brand guide/font/web/SKTSansDisplay-ExtraLight.woff2` | 제목체-ExtraLight | 359KB |
| `../brand guide/font/web/SKTSansDisplay-Light.woff2` | 제목체-Light | 454KB |
| `../brand guide/font/web/SKTSansDisplay-Regular.woff2` | 제목체-Regular | 459KB |
| `../brand guide/font/web/SKTSansDisplay-Bold.woff2` | 제목체-Bold | 467KB |
| `../brand guide/font/web/SKTSansDisplay-ExtraBold.woff2` | 제목체-ExtraBold | 400KB |
| `../brand guide/font/web/SKTSansDisplay-Braille.woff2` | 제목체-Braille | 90KB |
| `../brand guide/font/web/SKTSansText-Light.woff2` | 본문체-Light | 466KB |
| `../brand guide/font/web/SKTSansText-Regular.woff2` | 본문체-Regular | 474KB |
| `../brand guide/font/web/SKTSansText-SemiBold.woff2` | 본문체-SemiBold | 481KB |
| `../brand guide/font/web/SKTSansText-Bold.woff2` | 본문체-Bold | 482KB |
| `../brand guide/font/web/SKTSansText-ExtraBold.woff2` | 본문체-ExtraBold | 477KB |
| `../brand guide/font/web/SKTSansText-Braille.woff2` | 본문체-Braille | 90KB |

OTF 10.72MB → WOFF2 **4.59MB** (43%).

## 용량 관리

한글 폰트라 웨이트 하나가 **약 460KB**다. 글리프 12,276자.

- **쓰는 웨이트만 선언한다.** 5종을 다 걸면 2.3MB다. 전단지 도구는 보통 제목 Bold + 본문 Regular/Bold면 충분하다.
- 유니코드 **범위** 서브셋은 효과가 없다 — 현대 한글 전체(AC00–D7A3)를 남기면 467KB→441KB, 5%뿐이다.
  파일 용량의 대부분이 그 11,172자이기 때문이다. **줄이려면 음절 목록 자체를 줄여야 한다.**

## 서브셋 2종 — 전단지 도구 전용

전단지 원고는 폰트를 **파일 안에 품고** 나가야 한다. 아트보드가 격리된 프레임이라
네트워크로 웹폰트를 못 받고, 원고는 인쇄소로 건너가는 한 장짜리 파일이기 때문이다.
그래서 음절을 **KS X 1001 완성형 2,350자**로 잘라 2종만 만든다.

| 서브셋 | 원본 | 크기 | 쓰는 곳 |
|---|---|---|---|
| `../studio/font_display_bold.woff2` | 제목체-Bold | 467KB → **132KB** (28%) | 제목 |
| `../studio/font_text_semibold.woff2` | 본문체-SemiBold | 481KB → **127KB** (26%) | 본문 · 그 외 전부 |

```bash
python3 wiki/subset-font.py
```

`brand guide/font/web/` 의 원본을 잘라 `studio/` 에 넣는다. **원본이 brand guide/ 이고
studio/ 의 woff2 는 생성물이다.** `wiki/sync-studio.py` 가 번들에 넣을 때 `url()` 을
`data:` URI 로 바꿔 끼운다 — 아트보드 런타임이 CSS 의 `url()` 은 풀어 주지 않기 때문이다.

- 웨이트는 `font-weight: 100 900` 으로 넓게 선언한다. 브라우저가 가짜 볼드를 만들지 않게 하려는 것이다.
  그래서 본문은 웨이트와 무관하게 SemiBold 로 찍힌다 — [template.md](template.md) 3 의 본문 규정과 같다.
- **KS X 1001 밖 음절은 빠진다.** 확장 완성형(뷁·똠 따위)을 쓰면 그 글자만 시스템 서체로 떨어진다.
  전단지 카피에 쓸 일이 없어 이 선을 골랐다.
- 정말 줄이려면 **상용 한글 2350자로 제한**해야 한다 (467KB→**150KB**, 1/3).
  다만 매장명·인명에 상용 외 글자가 들어가면 **글자가 깨진다.** 임의 입력을 받는 도구에는 권하지 않는다.
- 첫 화면에 쓰는 웨이트는 `<link rel="preload" as="font" type="font/woff2" crossorigin>`로 미리 받는다.

## 금지 (brand.md 3.2)

- 가독이 어려운 넓은 행간 / 좁은 행간 / 좁은 자간
- 내용 전달을 방해하는 정렬 변형
