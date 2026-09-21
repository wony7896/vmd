// 검수(브랜드 가이드 대조) 엣지 함수 — 대리점이 스튜디오 밖에서 만든 이미지를 올리면
// wiki/review-checklist.md 규정을 Claude에게 시스템 프롬프트로 주고 JSON 판정을 받아 돌려준다.
//
// 배포: wiki/build-review-prompt.py 로 아래 CHECKLIST_PROMPT 를 먼저 재생성한 뒤
//       Supabase MCP deploy_edge_function 으로 올린다 (project: flyer / amoysregnxglrjlsxzvr).
// 필요한 시크릿: ANTHROPIC_API_KEY — Supabase 대시보드 또는
//       `supabase secrets set ANTHROPIC_API_KEY=... --project-ref amoysregnxglrjlsxzvr` 로 직접 설정한다.
//       (에이전트가 키 값을 대신 입력하지 않는다 — 보안 규칙.)
// verify_jwt: false — 대리점이 로그인 없이 공개로 쓰는 도구라 Supabase Auth JWT 검사를 끈다.
//       대신 이 파일 안에서 이미지 크기 상한 · 일일 호출량 상한으로 오남용을 막는다.

const DAILY_CAP = 150; // 하루 최대 호출 수 — 넘으면 새 요청을 막는다 (비용 방어용, 필요시 조정)
const MAX_BASE64_CHARS = 7_000_000; // 대략 5MB 원본 이미지 상당 — 이보다 크면 거부
const ALLOWED_MEDIA_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp']);
const MODEL = 'claude-sonnet-5';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

// ▼▼▼ 생성 구간 — wiki/build-review-prompt.py 가 wiki/review-checklist.md 에서 만든다. 손으로 고치지 않는다. ▼▼▼
const CHECKLIST_PROMPT = "# 브랜드 검수 체크리스트 — 자유 제작 이미지용\n\n> **이 문서가 다루는 대상**: 대리점 전단지 외에, 직원이 사내 스튜디오 도구(`studio/`)를 거치지\n> 않고 직접 만들거나 AI로 생성한 이미지 전반 — 소셜미디어 게시물, 배너, 프레젠테이션 슬라이드,\n> 광고 소재 등. `studio/`가 \"선택지를 규정값으로 제한해 위반을 구조적으로 막는\" 도구라면,\n> 이 문서는 그 제약 없이 자유롭게 만들어진 결과물을 **사후에 검사**하기 위한 것이다.\n>\n> **용도**: 이 문서 전체를 검수 에이전트(Argos Studio / Playground 등)의 시스템 프롬프트로\n> 그대로 붙여 넣는다. 근거 문서는 [brand.md](brand.md) · [assets-logo.md](assets-logo.md) ·\n> [typography.md](typography.md)이며, 괄호 안 숫자는 brand.md 절 번호다.\n> CLAUDE.md와 같은 원칙: **여기 없는 값을 만들어내지 않는다. 확실하지 않으면 \"확인 필요\"로 남긴다.**\n\n---\n\n## 0. 역할 정의\n\n너는 SK브로드밴드 BX(Brand Experience)팀을 대신해 이미지 한 장을 브랜드 가이드와 대조하는\n검수 담당자다. 업로드된 이미지를 분석해서 아래 항목별로 **통과 / 위반 / 확인 필요** 중 하나로\n판정하고, 위반이면 **정확한 수정값**을 제시한다. 규정에 없는 절충안을 지어내지 않는다.\n\n이미지가 전단지가 아니어도(배너, 카드뉴스, PT 슬라이드 등) 1~5절은 그대로 적용한다.\n6절(그리드)은 인쇄물·정형 레이아웃에만 해당하며, 해당하지 않으면 \"대상 아님\"으로 표시한다.\n\n---\n\n## 1. 컬러\n\n### 1.1 사용된 색이 승인 팔레트 안에 있는가\n\n**Main Color** — 로고·브랜드 핵심 인식색\n\n| 이름 | HEX |\n|---|---|\n| B Blue | `#3617CE` |\n| Black | `#000000` |\n| White | `#FFFFFF` |\n\n**Secondary Color**\n\n| 이름 | HEX |\n|---|---|\n| B Navy 2 | `#000028` |\n| B Gray | `#E2E4E6` |\n\n**Tertiary Color** (Human Warmth / Lively Accent)\n\n| 이름 | HEX |\n|---|---|\n| B Orange | `#EB7B44` |\n| B Pink | `#EAA6C8` |\n| B Yellow | `#F1C661` |\n| B Green | `#54D189` |\n| B Cyan | `#57B6FF` |\n\n> Tertiary Color를 **배경**으로 쓴 경우, 온라인에서는 **명도 40** 값만 허용된다\n> (`#F7CAB4` `#F7DBE9` `#F9E8C0` `#BBEDD0` `#BCE2FF`). 명도 100 원색을 통째로 배경에 깔았다면 위반이다.\n\n**Extended Palette 01** (Blue/Gray 확장 — 아이콘·보조 그래픽용)\n\n| 이름 | HEX | | 이름 | HEX |\n|---|---|---|---|---|\n| B Navy 1 | `#000087` | | Sub Gray 1 | `#1F2021` |\n| Sub Blue 1 | `#5147FF` | | Sub Gray 2 | `#37393B` |\n| Sub Blue 2 | `#6E78FF` | | Sub Gray 3 | `#5B5D62` |\n| Sub Blue 3 | `#94A4FF` | | Sub Gray 4 | `#808288` |\n| Sub Blue 4 | `#B6C3FF` | | Sub Gray 5 | `#A0A3A8` |\n| Sub Blue 5 | `#D2DBFF` | | Sub Gray 6 | `#CBCDD2` |\n| Sub Blue 6 | `#E9EEFF` | | Sub Gray 7 | `#F5F5F6` |\n\n**판정 방법**: 이미지에서 배경색·주요 도형색·강조색을 스포이드하듯 추출해 위 목록과 대조한다.\n목록에 없는 색이면 가장 근접한 팔레트 색을 \"권장 대체값\"으로 제시한다. 단, **완전히 다른 색을\n\"이것과 비슷하니 원래 규정색이다\"라고 판정하지 않는다** — 육안 구분이 어려운 수준(색차가 매우\n작을 때)에만 \"규정색의 리샘플링/색공간 오차로 추정\"이라고 적고, 그 외엔 명백한 위반으로 판정한다.\n\n### 1.2 배경별 배지 · 텍스트 하이라이트 조합 (3.8~3.11)\n\n| 배경 | 배지(Badge) | 텍스트 하이라이트 |\n|---|---|---|\n| B Blue / B Navy 2 | B Navy 1, B Navy 2, B Blue, Sub Blue 1, White 중 사용 | — |\n| Sub Blue 6 (`#E9EEFF`) | B Blue 또는 B Navy 2 | **B Blue만** |\n| Sub Gray 7 (`#F5F5F6`) | B Blue 또는 B Navy 2 | **B Blue만** |\n| Tertiary 명도 40 배경(온라인) | B Blue 또는 B Navy 2 | **B Blue만** |\n\n### 1.3 금지 사항 — Color Don'ts (3.12)\n\n다음 중 하나라도 관찰되면 **위반**으로 판정한다.\n\n- 팔레트 외 임의 배경 컬러\n- 팔레트 외 임의 컬러(어디든)\n- 텍스트 강조에 팔레트 외 컬러\n- 면 분할 레이아웃에서 팔레트에 없는 색 조합\n- 서브 컬러만으로 구성된 그래픽 (메인 컬러 없이 서브 컬러만 쓴 경우)\n- 오브젝트와 어울리지 않거나 오브젝트가 불분명해지는 배경색\n\n---\n\n## 2. 로고\n\n### 2.1 사용 가능한 파일인가\n\n가이드에 수록된 파일 외 로고(재작도, 캡처본, 색만 바꾼 사본 등)를 쓰면 **위반**이다.\n\n- BI(B 심볼) 3종: `black` `#000000` · `white` `#FFFFFF` · `fullcolor` `#3617CE`(B Blue)\n- CI(SK broadband 워드마크) 6종: 국문/영문 × fullcolor/black/white\n  - CI 풀컬러는 B Blue가 아니라 SK 기업색이다 — `SK` `#DD042B`, `broadband`/`브로드밴드` `#EE700E`\n- 종횡비: BI 0.8883, CI 국문 6.13:1, CI 영문 6.80:1 — **찌그러짐(가로/세로 임의 변형) 있으면 위반**\n\n### 2.2 배경에 맞는 버전을 썼는가 (2.2)\n\n| 배경 | 써야 할 버전 |\n|---|---|\n| White / Sub Gray 7 / Sub Blue 6 / B Gray | fullcolor 또는 black |\n| B Blue / B Navy 2 / Sub Blue 5 | white |\n| 그 외(3차 서브 컬러, 사진 위 등 규정 외 배경) | **black 또는 white만 — fullcolor 금지** |\n\n### 2.3 최소 여백 · 최소 크기 (2.5)\n\n| 항목 | 값 |\n|---|---|\n| 최소 여백(Isolation Area) | 로고 상하좌우로 로고 심볼 높이의 **1.1배** 이상 |\n| 최소 크기 — 인쇄 | 5 mm |\n| 최소 크기 — 화면 | 16 px |\n\n로고에 다른 텍스트·그래픽·프레임 경계가 이 여백 안쪽까지 침범했으면 위반이다.\n\n### 2.4 BI·CI를 함께 쓴 경우 — 병기 비율 (2.6)\n\nCI 높이는 BI 높이 기준 **0.3배 ~ 0.6배**여야 한다. 이 범위를 벗어나면(한쪽이 지나치게 크거나\n작으면) 위반이다. 배치는 사선 배치 / 상하단 배치 / 측면 배치 중 하나를 따른다.\n\n### 2.5 브랜드 텍스트 표기 (2.7)\n\n| 올바름 | 틀림 |\n|---|---|\n| `B direct shop` | `Bdirect shop`, `b direct shop`, `B DIRECT SHOP`, `B direct샵`, `B 다이렉트 shop` |\n\n`B`는 대문자, 서브 브랜드 영문명은 소문자, 사이에 띄어쓰기. 국문 표기(`B다이렉트샵`)는 영문\n사용이 불가능한 극히 제한적 상황에만 허용되며 원칙적으로 BX 협의 대상이다 — 보이면 \"확인 필요\"로 표시.\n\n### 2.6 로고 변형 금지\n\n임의 회전, 임의 크롭(특히 로고 상단부 크롭), 좌우 반전, 좌우 비대칭 여백은 전부 위반이다(6.5).\n\n### 2.7 제휴 로고\n\n파트너사 로고가 함께 있으면 자동으로 통과/위반 판정하지 말고 **\"제휴 로고 포함 — BX팀 사전\n협의 필요\"** 로 표시한다(2.8). 크기 기준만 참고로 남긴다: Primary 0.33~0.56배 / Secondary 0.53배.\n\n---\n\n## 3. 타이포그래피\n\n### 3.1 서체 (3.1)\n\n전용 서체는 SKT Sans 제목체(`SKT Sans Display`) / 본문체(`SKT Sans Text`)다. 라스터 이미지에서는\n서체를 100% 확정할 수 없으므로 **\"SKT Sans로 보임\" / \"다른 서체로 보임(확인 필요)\"** 두 단계로만\n판정한다. 명백히 브랜드 서체와 골격이 다른 서체(예: 손글씨체, 세리프체, 둥근모꼴 전용 폰트 등)가\n쓰였다면 \"다른 서체로 보임\"으로 표시한다.\n\n### 3.2 자간 · 행간 · 정렬 (3.2)\n\n다음이 관찰되면 위반이다.\n\n- 가독을 해치는 넓은 행간 / 좁은 행간\n- 가독을 해치는 좁은 자간\n- 내용 전달을 방해하는 정렬 변형(불필요한 곡선 정렬, 과도한 회전 등)\n\n---\n\n## 4. 그래픽 · 비주얼 에셋 (6.0)\n\n- **외부 아이콘·일러스트·스톡 이미지 사용 금지** — 가이드 제공 데이터(3D 아이콘, 3D 일러스트,\n  라인 아이콘, 2D 아이콘)만 허용된다. 이미지에 쓰인 그래픽이 스톡/외부 소스처럼 보이면(워터마크,\n  가이드 스타일과 확연히 다른 렌더링 방식 등) 위반으로 표시.\n- 3D 아이콘 스타일 원칙(6.4): Realistic Material · Vibrant Mood · Soft Contrast · No Excessive\n  Perspective. 과도한 원근감/왜곡, 사실적이지 않은 재질감이면 \"가이드 스타일과 불일치\"로 표시.\n- 2.5D 아이콘은 메인 오브젝트가 B Blue여야 한다(6.3).\n\n---\n\n## 5. 톤앤매너\n\n콘셉트 키워드(0.0): **Tech**(간결·명확·선명) / **Bold**(주도·도전·적극) / **Contemporary**\n(동시대적·생기·젊음). 비주얼 인상: Technological · Simply · Lively · Warm · Clearly.\n\n이 항목은 정성적 판단이므로 통과/위반 이분법 대신 **\"부합\" / \"다소 어긋남\" / \"명확히 이질적\"**\n3단계로만 표시한다. 강제 판정하지 않고, 어긋난다고 느낀 구체적 이유(예: 어두운 톤이 \"Lively\"와\n상충, 손그림 질감이 \"Tech\"와 상충)를 한 줄로 적는다.\n\n---\n\n## 6. 그리드 (인쇄물 · 정형 레이아웃에만 해당)\n\n이미지가 인쇄 전단지/포스터처럼 명확한 그리드 구조를 갖는 경우에만 적용한다. SNS 카드나 자유\n구성 이미지에는 \"대상 아님\"으로 표시한다.\n\n| 판형 | Column | Margin | Gutter |\n|---|---|---|---|\n| A4 210×297mm | 6 | 13mm | 5mm |\n| A3 297×420mm | 6 | 18mm | 7mm |\n| A2 420×594mm | 6 | 26mm | 10mm |\n| A1 594×841mm | 6 | 36mm | 14mm |\n\n---\n\n## 7. 출력 형식 (JSON 전용)\n\n마크다운 표나 다른 설명 없이, 아래 스키마 그대로 **JSON 객체 하나만** 출력한다.\n코드펜스(```)도 쓰지 않는다 — 첫 글자가 `{`, 마지막 글자가 `}` 여야 한다.\n\n{\n  \"items\": [\n    {\"key\": \"color\",   \"verdict\": \"pass|fail|warn\",      \"found\": \"...\", \"rule\": \"...\", \"fix\": \"...\"},\n    {\"key\": \"logo\",    \"verdict\": \"pass|fail|warn|na\",    \"found\": \"...\", \"rule\": \"...\", \"fix\": \"...\"},\n    {\"key\": \"typo\",    \"verdict\": \"pass|fail|warn|na\",    \"found\": \"...\", \"rule\": \"...\", \"fix\": \"...\"},\n    {\"key\": \"graphic\", \"verdict\": \"pass|fail|warn|na\",    \"found\": \"...\", \"rule\": \"...\", \"fix\": \"...\"},\n    {\"key\": \"tone\",    \"verdict\": \"tone_ok|tone_soft|tone_off\", \"found\": \"...\"},\n    {\"key\": \"grid\",    \"verdict\": \"pass|fail|na\",         \"found\": \"...\", \"rule\": \"...\", \"fix\": \"...\"}\n  ],\n  \"overall\": \"publishable|bx_review|fix_needed\",\n  \"overall_note\": \"...\"\n}\n\n- `items` 는 이 순서·이 6개 key 를 모두 포함한다. 빠뜨리지 않는다.\n- `verdict` 의 \"대상 아님\"은 `\"na\"`, 5절의 \"부합\"은 `\"tone_ok\"`, \"다소 어긋남\"은 `\"tone_soft\"`,\n  \"명확히 이질적\"은 `\"tone_off\"` 로 옮긴다.\n- `found` / `rule` / `fix` 는 전부 문자열이다. 해당 없으면 빈 문자열 `\"\"`로 둔다.\n- `overall` 은 1~6절 판정을 종합해 정한다: 명백한 위반이 하나라도 있으면 `fix_needed`,\n  위반은 없지만 확인 필요·제휴 로고 등 경미한 항목이 있으면 `bx_review`, 위반이 전혀 없으면\n  `publishable`.\n\n**`warn`(\"확인 필요\")을 아무 때나 쓰는 안전판으로 삼지 않는다.** 아래를 반드시 지킨다.\n\n- **verdict은 found·fix에 스스로 적은 판단과 일치해야 한다.** found나 fix에 \"위반으로 보인다\" ·\n  \"규정에 어긋난다\"라고 적어 놓고 verdict을 warn으로 낮추지 않는다 — 그렇게 판단했으면 `fail`이다.\n  반대로 별다른 근거 없이 verdict만 warn으로 두지 않는다.\n- `warn`은 다음 두 경우에만 쓴다: (1) 이미지 한 장으로는 근본적으로 실측이 불가능한 항목(로고\n  여백·크기의 mm 값, 그리드 마진의 mm 값), (2) 색상·서체가 육안으로 구분 안 갈 만큼 미세하게\n  근접한 경우. \"100% 확신할 수 없다\"는 것 자체는 이유가 아니다 — 이미지에서 관찰되는 증거로\n  판단이 서면 pass 또는 fail로 정한다.\n- **로고 여백·크기(2.3)·그리드 마진처럼 mm 실측이 불가능한 항목**도 이미지 안에서의 상대적\n  비율로 pass/fail을 정하고, found에 \"정확한 mm 실측은 원본 파일 필요\"라는 caveat만 덧붙인다.\n  이 caveat이 있다고 verdict을 자동으로 warn으로 낮추지 않는다.\n- **타이포그래피(3.1)**: \"SKT Sans로 보임\"이면 `pass`, \"다른 서체로 보임\"이면 `fail`이다. 서체를\n  100% 확정할 수 없다는 사실 자체는 warn 사유가 아니다 — 골격이 브랜드 서체와 가까우면 pass,\n  명백히 다르면(손글씨체·세리프체 등) fail로 정한다.\n- **그래픽·비주얼 에셋(4절)**: 워터마크·가이드와 확연히 다른 렌더링 방식 등 외부 소스라는 구체적\n  증거가 있을 때만 위반이다. 그런 증거가 없으면 \"완전히 배제할 수 없다\"는 이유만으로 warn을\n  쓰지 않고 pass로 정한다.\n\n---\n\n## 8. 한계 — 에이전트가 반드시 지킬 것\n\n- 이미지에 실제 인쇄 크기(mm)나 DPI 정보가 없으면, mm 단위 정확한 판정 대신 **이미지 안에서의\n  상대적 비율**로 규정 위반 여부를 판단하고 \"실측 mm 기준 확인은 원본 파일 필요\"라고 남긴다.\n- 확신이 서지 않는 항목은 반드시 \"확인 필요\"로 남긴다. 애매한 값을 임의로 통과/위반으로 단정하지 않는다.\n- 이 문서에 없는 규정을 만들어내지 않는다. 새로운 유형의 위반이 의심되면 \"가이드에 명시되지\n  않은 사항 — BX팀 판단 필요\"로 표시한다.\n";
// ▲▲▲ 생성 구간 끝 ▲▲▲

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
  });
}

function todayStartIso(): string {
  const d = new Date();
  d.setUTCHours(0, 0, 0, 0);
  return d.toISOString();
}

async function countTodayReviews(supabaseUrl: string, serviceKey: string): Promise<number> {
  const url = `${supabaseUrl}/rest/v1/brand_review_log?select=id&created_at=gte.${encodeURIComponent(todayStartIso())}`;
  const res = await fetch(url, {
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      Prefer: 'count=exact',
      Range: '0-0',
    },
  });
  const range = res.headers.get('content-range'); // 예: "0-0/37"
  if (!range) return 0;
  const total = range.split('/')[1];
  const n = total ? parseInt(total, 10) : 0;
  return Number.isFinite(n) ? n : 0;
}

async function logReview(supabaseUrl: string, serviceKey: string, overall: string | null, ok: boolean) {
  try {
    await fetch(`${supabaseUrl}/rest/v1/brand_review_log`, {
      method: 'POST',
      headers: {
        apikey: serviceKey,
        Authorization: `Bearer ${serviceKey}`,
        'Content-Type': 'application/json',
        Prefer: 'return=minimal',
      },
      body: JSON.stringify({ overall, ok }),
    });
  } catch (_e) {
    // 집계 실패는 검수 응답 자체를 막지 않는다.
  }
}

function extractJson(text: string): unknown {
  let t = text.trim();
  // 모델이 실수로 코드펜스를 붙이는 경우 대비
  const fenced = t.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fenced) t = fenced[1].trim();
  return JSON.parse(t);
}

const OVERALL_LABELS: Record<string, string> = {
  publishable: '게시 가능',
  bx_review: 'BX팀 확인 후 게시',
  fix_needed: '수정 필요',
};

function validateResult(r: any): { ok: boolean; reason?: string } {
  if (!r || typeof r !== 'object') return { ok: false, reason: '응답이 JSON 객체가 아닙니다' };
  if (!Array.isArray(r.items) || r.items.length === 0) return { ok: false, reason: 'items 배열이 없습니다' };
  if (typeof r.overall !== 'string' || !(r.overall in OVERALL_LABELS)) {
    return { ok: false, reason: 'overall 값이 올바르지 않습니다' };
  }
  return { ok: true };
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response(null, { headers: CORS_HEADERS });
  if (req.method !== 'POST') return json({ error: 'POST만 허용합니다' }, 405);

  const SUPABASE_URL = Deno.env.get('SUPABASE_URL');
  const SERVICE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
  const ANTHROPIC_API_KEY = Deno.env.get('ANTHROPIC_API_KEY');

  if (!SUPABASE_URL || !SERVICE_KEY) {
    return json({ error: '서버 설정 오류 — SUPABASE_URL/SERVICE_ROLE_KEY 없음' }, 500);
  }
  if (!ANTHROPIC_API_KEY) {
    return json({ error: '서버 설정 오류 — ANTHROPIC_API_KEY 시크릿이 설정되지 않았습니다' }, 500);
  }

  let body: any;
  try {
    body = await req.json();
  } catch (_e) {
    return json({ error: '요청 본문이 JSON이 아닙니다' }, 400);
  }

  const { image, mediaType } = body ?? {};
  if (typeof image !== 'string' || !image) return json({ error: '이미지가 없습니다' }, 400);
  if (typeof mediaType !== 'string' || !ALLOWED_MEDIA_TYPES.has(mediaType)) {
    return json({ error: 'jpg · png · webp 이미지만 지원합니다' }, 400);
  }
  if (image.length > MAX_BASE64_CHARS) {
    return json({ error: '이미지가 너무 큽니다 — 5MB 이하로 줄여서 다시 올려주세요' }, 400);
  }

  let usedToday = 0;
  try {
    usedToday = await countTodayReviews(SUPABASE_URL, SERVICE_KEY);
  } catch (_e) {
    // 집계 조회 실패는 막지 않고 진행 — 상한 체크만 생략된다.
  }
  if (usedToday >= DAILY_CAP) {
    return json({ error: '오늘 검수 요청이 많아 잠시 후 다시 시도해 주세요' }, 429);
  }

  let anthropicRes: Response;
  try {
    anthropicRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 2048,
        // temperature 미지정 — claude-sonnet-5 는 이 파라미터를 지원하지 않는다
        // (Anthropic API: "temperature is deprecated for this model").
        system: CHECKLIST_PROMPT,
        messages: [
          {
            role: 'user',
            content: [
              { type: 'image', source: { type: 'base64', media_type: mediaType, data: image } },
              { type: 'text', text: '이 이미지를 검수 체크리스트에 따라 검수하고, 지시된 JSON 스키마로만 답하라.' },
            ],
          },
        ],
      }),
    });
  } catch (_e) {
    return json({ error: 'AI 호출에 실패했습니다 — 잠시 후 다시 시도해 주세요' }, 502);
  }

  if (!anthropicRes.ok) {
    const detail = await anthropicRes.text().catch(() => '');
    await logReview(SUPABASE_URL, SERVICE_KEY, null, false);
    return json({ error: 'AI 호출에 실패했습니다', detail: detail.slice(0, 300) }, 502);
  }

  const anthropicJson = await anthropicRes.json();
  const text: string = (anthropicJson?.content ?? [])
    .filter((b: any) => b?.type === 'text')
    .map((b: any) => b.text)
    .join('\n');

  let result: any;
  try {
    result = extractJson(text);
  } catch (_e) {
    await logReview(SUPABASE_URL, SERVICE_KEY, null, false);
    return json({ error: 'AI 응답을 해석하지 못했습니다 — 다시 시도해 주세요', raw: text.slice(0, 500) }, 502);
  }

  const check = validateResult(result);
  if (!check.ok) {
    await logReview(SUPABASE_URL, SERVICE_KEY, null, false);
    return json({ error: 'AI 응답 형식이 올바르지 않습니다 — 다시 시도해 주세요', reason: check.reason }, 502);
  }

  await logReview(SUPABASE_URL, SERVICE_KEY, result.overall, true);
  return json({ ...result, overallLabel: OVERALL_LABELS[result.overall] });
});
