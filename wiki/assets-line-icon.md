# 라인 · 2D 아이콘 인덱스

> 원본: `../brand guide/Line Icon/Line Icon_fin.pdf` (5p, 벡터)
> 추출본: `../brand guide/Line Icon/png/` — **210개, 투명 PNG**
> 규정: [brand.md](brand.md) 6.1 (8.1~8.2)
> 갱신 2026-09-15 · **라벨 210/210 확정**

## 이 파일들은 어디서 왔나

원본은 **아이콘이 개별 파일로 존재하지 않았다.** 1920×1080 슬라이드 5장 안에 격자로 배치돼 있어
그대로는 전단지에 쓸 수 없었다. PDF의 벡터 데이터에서 격자를 검출해 210개를 잘라내고,
뒤에 깔린 **설계 가이드 격자(회색·시안)를 제거해 투명 PNG로** 저장했다.

| 항목 | 값 |
|---|---|
| 개수 | 210 |
| 포맷 | PNG · 알파 채널 · 검정 단색 |
| 해상도 | 원본 18배 렌더 |
| 용량 | 합계 약 4.4MB |

> **색을 바꾸려면 원본 `.ai`에서 다시 뽑아야 한다.** 추출본은 검정 단색이다.
> 벡터(SVG) 추출도 시도했으나 PDF 패스의 채움 규칙이 정확히 복원되지 않아 래스터를 택했다.
> SVG가 필요하면 Illustrator에서 `Line Icon_fin.ai`를 열어 **에셋 내보내기**로 일괄 추출하는 편이 정확하다.

## 라벨은 어떻게 확정했나

원본 슬라이드의 라벨 텍스트가 **아웃라인 처리**돼 있어 PDF·AI 어느 쪽에서도 문자로 추출되지 않는다.
라벨 영역을 고배율로 렌더해 macOS Vision OCR을 돌리고, **그 결과와 육안 판독을 서로 대조**해 확정했다.
둘이 어긋난 25건과 OCR이 못 읽은 62건은 개별 확대해 확인했다. 그 과정에서 아래를 바로잡았다.

| 파일 | 오독 | 확정 |
|---|---|---|
| `line-113 / line-114` | 할아버지 / 할머니 | **할머니 / 할아버지** (서로 뒤바뀜) |
| `line-131` | 킥보드 | 전동 스쿠터 |
| `line-132` | 배송 | 배송 트럭 |
| `line-145` | 비상 | 비상벨 |
| `line-146` | 타게팅 | 타겟팅 |
| `line-169` | 업로드 | 업그레이드 |
| `line-171 / line-172` | 좋아요 / 싫어요 | Good / Bad |
| `line-177` | 하트 | 좋아요 |
| `line-190` | 비대면 | 비대면 상담 |
| `line-196` | The Park | Theme Park |

> `line-162`와 `line-175`는 **둘 다 라벨이 «질문»** 이다. 원본이 그렇다. 아이콘은 서로 다르다
> (물음표 원형 / Q 말풍선).

## 사용 규칙

1. 라인 아이콘은 **UI·정보 전달용**이다. 전단지 주력은 3D 아이콘([assets-icon.md](assets-icon.md))이다.
2. 규격(brand.md 6.1): Design Area 16dp, Padding 상하좌우 2dp **필수**, Total 20dp, 선 굵기 0.85dp / 사선 120°.
3. 추출본에는 패딩이 포함돼 있다. 배치할 때 추가 여백을 더 주지 않는다.
4. 파일 번호는 원본 슬라이드의 배치 순서(좌→우, 위→아래)와 같다.

---


## 1) B world

> 용도: 서비스 진입·안내 — 앱/웹 UI 중심

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-001.png` | 홈 |
| `../brand guide/Line Icon/png/line-002.png` | 메뉴 |
| `../brand guide/Line Icon/png/line-003.png` | 로그인 |
| `../brand guide/Line Icon/png/line-004.png` | 설정 |
| `../brand guide/Line Icon/png/line-005.png` | 챗봇 |
| `../brand guide/Line Icon/png/line-006.png` | 고객지원 |
| `../brand guide/Line Icon/png/line-007.png` | 상품서비스 |
| `../brand guide/Line Icon/png/line-008.png` | B다이렉트샵 |
| `../brand guide/Line Icon/png/line-009.png` | 고객지원 |
| `../brand guide/Line Icon/png/line-010.png` | 원격 점검 |
| `../brand guide/Line Icon/png/line-011.png` | B tv |
| `../brand guide/Line Icon/png/line-012.png` | B tv pop |
| `../brand guide/Line Icon/png/line-013.png` | B tv cable |
| `../brand guide/Line Icon/png/line-014.png` | 인터넷 |
| `../brand guide/Line Icon/png/line-015.png` | 기가인터넷 |
| `../brand guide/Line Icon/png/line-016.png` | 500Mbps 인터넷 |
| `../brand guide/Line Icon/png/line-017.png` | 기가와이파이 |
| `../brand guide/Line Icon/png/line-018.png` | 윙즈 |
| `../brand guide/Line Icon/png/line-019.png` | TV+인터넷 |
| `../brand guide/Line Icon/png/line-020.png` | 인터넷+ADT캡스 |

## 2) Telco

> 용도: 통신 상품·요금·데이터 소구

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-021.png` | 음성통화 |
| `../brand guide/Line Icon/png/line-022.png` | 통화품질 |
| `../brand guide/Line Icon/png/line-023.png` | 영상통화 |
| `../brand guide/Line Icon/png/line-024.png` | 로밍 |
| `../brand guide/Line Icon/png/line-025.png` | 음성 컬러링 |
| `../brand guide/Line Icon/png/line-026.png` | 영상 컬러링 |
| `../brand guide/Line Icon/png/line-027.png` | 기지국 |
| `../brand guide/Line Icon/png/line-028.png` | LTE |
| `../brand guide/Line Icon/png/line-029.png` | 5G |
| `../brand guide/Line Icon/png/line-030.png` | 속도 측정기 |
| `../brand guide/Line Icon/png/line-031.png` | 문자메시지 |
| `../brand guide/Line Icon/png/line-032.png` | 요금 |
| `../brand guide/Line Icon/png/line-033.png` | 보험 |
| `../brand guide/Line Icon/png/line-034.png` | 인증 |
| `../brand guide/Line Icon/png/line-035.png` | MB |
| `../brand guide/Line Icon/png/line-036.png` | GB |
| `../brand guide/Line Icon/png/line-037.png` | 휴대폰 요금 |
| `../brand guide/Line Icon/png/line-038.png` | 휴대폰 검색 |
| `../brand guide/Line Icon/png/line-039.png` | 휴대폰 결합 |
| `../brand guide/Line Icon/png/line-040.png` | 휴대폰 할인 |
| `../brand guide/Line Icon/png/line-041.png` | 휴대폰 데이터 |
| `../brand guide/Line Icon/png/line-042.png` | 휴대폰 보험 |
| `../brand guide/Line Icon/png/line-043.png` | 휴대폰 수리 |
| `../brand guide/Line Icon/png/line-044.png` | 충전 |
| `../brand guide/Line Icon/png/line-045.png` | 데이터 |
| `../brand guide/Line Icon/png/line-046.png` | 데이터 무제한 |
| `../brand guide/Line Icon/png/line-047.png` | 데이터 결합 |
| `../brand guide/Line Icon/png/line-048.png` | 데이터 충전 |
| `../brand guide/Line Icon/png/line-049.png` | 스마트홈 할인 |
| `../brand guide/Line Icon/png/line-050.png` | 스마트홈 결합 |

## 3) Electronics

> 용도: 단말·기기 안내

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-051.png` | 전화기 |
| `../brand guide/Line Icon/png/line-052.png` | 스마트폰 |
| `../brand guide/Line Icon/png/line-053.png` | 컴퓨터 |
| `../brand guide/Line Icon/png/line-054.png` | 태블릿 |
| `../brand guide/Line Icon/png/line-055.png` | TV |
| `../brand guide/Line Icon/png/line-056.png` | VR 기기 |
| `../brand guide/Line Icon/png/line-057.png` | 스마트워치 |
| `../brand guide/Line Icon/png/line-058.png` | 게임기 |
| `../brand guide/Line Icon/png/line-059.png` | 카메라 |
| `../brand guide/Line Icon/png/line-060.png` | 셋톱박스 |
| `../brand guide/Line Icon/png/line-061.png` | 이어폰 |
| `../brand guide/Line Icon/png/line-062.png` | 헤드폰 |
| `../brand guide/Line Icon/png/line-063.png` | AI 스피커 |
| `../brand guide/Line Icon/png/line-064.png` | 공기청정기 |
| `../brand guide/Line Icon/png/line-065.png` | 정수기 |
| `../brand guide/Line Icon/png/line-066.png` | 커피머신 |
| `../brand guide/Line Icon/png/line-067.png` | 드론 |

## 4) Benefit

> 용도: 혜택·할인·경품 강조

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-068.png` | 쿠폰 |
| `../brand guide/Line Icon/png/line-069.png` | 할인_01 |
| `../brand guide/Line Icon/png/line-070.png` | 할인_02 |
| `../brand guide/Line Icon/png/line-071.png` | 선물 |
| `../brand guide/Line Icon/png/line-072.png` | 경품_01 |
| `../brand guide/Line Icon/png/line-073.png` | 경품_02 |
| `../brand guide/Line Icon/png/line-074.png` | 포인트 |
| `../brand guide/Line Icon/png/line-075.png` | FREE |
| `../brand guide/Line Icon/png/line-076.png` | 1+1 |
| `../brand guide/Line Icon/png/line-077.png` | 무제한 |

## 5) Membership

> 용도: 가입·상담·계약·VIP

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-078.png` | 고객 |
| `../brand guide/Line Icon/png/line-079.png` | 고객 정보 |
| `../brand guide/Line Icon/png/line-080.png` | 신규가입_01 |
| `../brand guide/Line Icon/png/line-081.png` | 신규가입_02 |
| `../brand guide/Line Icon/png/line-082.png` | 상담 |
| `../brand guide/Line Icon/png/line-083.png` | VIP_01 |
| `../brand guide/Line Icon/png/line-084.png` | VIP_02 |
| `../brand guide/Line Icon/png/line-085.png` | 카드 발급 |
| `../brand guide/Line Icon/png/line-086.png` | 카드 할인 |
| `../brand guide/Line Icon/png/line-087.png` | VIP 카드 |
| `../brand guide/Line Icon/png/line-088.png` | 신규 계약 |
| `../brand guide/Line Icon/png/line-089.png` | 계약 완료 |
| `../brand guide/Line Icon/png/line-090.png` | 계약 변경 |
| `../brand guide/Line Icon/png/line-091.png` | 계약 정보 |
| `../brand guide/Line Icon/png/line-092.png` | 계약 확인 |

## 6) Business

> 용도: 콘텐츠·서비스 영역

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-093.png` | Mobility_01 |
| `../brand guide/Line Icon/png/line-094.png` | Mobility_02 |
| `../brand guide/Line Icon/png/line-095.png` | VOD |
| `../brand guide/Line Icon/png/line-096.png` | Music |
| `../brand guide/Line Icon/png/line-097.png` | Game |
| `../brand guide/Line Icon/png/line-098.png` | Movie |
| `../brand guide/Line Icon/png/line-099.png` | E-Book |
| `../brand guide/Line Icon/png/line-100.png` | Health-care |
| `../brand guide/Line Icon/png/line-101.png` | E-Commerce |
| `../brand guide/Line Icon/png/line-102.png` | AR/VR |

## 7) Technology

> 용도: 기술 소구

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-103.png` | 얼굴 인식 |
| `../brand guide/Line Icon/png/line-104.png` | 지문 인식 |
| `../brand guide/Line Icon/png/line-105.png` | 홍채 인식 |
| `../brand guide/Line Icon/png/line-106.png` | 로봇 기술 |
| `../brand guide/Line Icon/png/line-107.png` | 블록체인 |
| `../brand guide/Line Icon/png/line-108.png` | 클라우드 |
| `../brand guide/Line Icon/png/line-109.png` | 보안 |
| `../brand guide/Line Icon/png/line-110.png` | 바이오 |
| `../brand guide/Line Icon/png/line-111.png` | 인공지능 |
| `../brand guide/Line Icon/png/line-112.png` | 스마트홈 |

## 8) People

> 용도: 대상 고객층 표시

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-113.png` | 할머니 |
| `../brand guide/Line Icon/png/line-114.png` | 할아버지 |
| `../brand guide/Line Icon/png/line-115.png` | 엄마 |
| `../brand guide/Line Icon/png/line-116.png` | 아빠 |
| `../brand guide/Line Icon/png/line-117.png` | 어린이(여) |
| `../brand guide/Line Icon/png/line-118.png` | 어린이(남) |
| `../brand guide/Line Icon/png/line-119.png` | 학생(여) |
| `../brand guide/Line Icon/png/line-120.png` | 학생(남) |
| `../brand guide/Line Icon/png/line-121.png` | 외국인 |
| `../brand guide/Line Icon/png/line-122.png` | 가족 |

## 9) Transportation

> 용도: 이동·배송

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-123.png` | 자동차_01 |
| `../brand guide/Line Icon/png/line-124.png` | 자동차_02 |
| `../brand guide/Line Icon/png/line-125.png` | 기차 |
| `../brand guide/Line Icon/png/line-126.png` | 지하철 |
| `../brand guide/Line Icon/png/line-127.png` | 버스_01 |
| `../brand guide/Line Icon/png/line-128.png` | 버스_02 |
| `../brand guide/Line Icon/png/line-129.png` | 비행기 |
| `../brand guide/Line Icon/png/line-130.png` | 자전거 |
| `../brand guide/Line Icon/png/line-131.png` | 전동 스쿠터 |
| `../brand guide/Line Icon/png/line-132.png` | 배송 트럭 |

## 10) Location

> 용도: 장소·설치 환경

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-133.png` | 집 |
| `../brand guide/Line Icon/png/line-134.png` | 학교 |
| `../brand guide/Line Icon/png/line-135.png` | 건물 |
| `../brand guide/Line Icon/png/line-136.png` | 스토어 |
| `../brand guide/Line Icon/png/line-137.png` | 은행 |
| `../brand guide/Line Icon/png/line-138.png` | 병원 |
| `../brand guide/Line Icon/png/line-139.png` | 편의점 |
| `../brand guide/Line Icon/png/line-140.png` | 공장 |

## 11) Object

> 용도: 사물·수단

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-141.png` | 카드 |
| `../brand guide/Line Icon/png/line-142.png` | 서류 |
| `../brand guide/Line Icon/png/line-143.png` | 지폐 |
| `../brand guide/Line Icon/png/line-144.png` | 알림벨 |
| `../brand guide/Line Icon/png/line-145.png` | 비상벨 |
| `../brand guide/Line Icon/png/line-146.png` | 타겟팅 |
| `../brand guide/Line Icon/png/line-147.png` | 자물쇠 |
| `../brand guide/Line Icon/png/line-148.png` | 트로피 |
| `../brand guide/Line Icon/png/line-149.png` | 룰렛 |
| `../brand guide/Line Icon/png/line-150.png` | 장바구니 |
| `../brand guide/Line Icon/png/line-151.png` | 알람시계 |
| `../brand guide/Line Icon/png/line-152.png` | 캘린더 |
| `../brand guide/Line Icon/png/line-153.png` | 지도 |
| `../brand guide/Line Icon/png/line-154.png` | 연필 |
| `../brand guide/Line Icon/png/line-155.png` | 책 |
| `../brand guide/Line Icon/png/line-156.png` | 확성기 |
| `../brand guide/Line Icon/png/line-157.png` | 열쇠 |
| `../brand guide/Line Icon/png/line-158.png` | 마이크 |
| `../brand guide/Line Icon/png/line-159.png` | 약 |
| `../brand guide/Line Icon/png/line-160.png` | 전구 |

## 12) Action

> 용도: 행동 유도(CTA)·상태

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-161.png` | 경고 |
| `../brand guide/Line Icon/png/line-162.png` | 질문 |
| `../brand guide/Line Icon/png/line-163.png` | 추가 |
| `../brand guide/Line Icon/png/line-164.png` | 완료 |
| `../brand guide/Line Icon/png/line-165.png` | 할인 |
| `../brand guide/Line Icon/png/line-166.png` | 화살표 |
| `../brand guide/Line Icon/png/line-167.png` | 다운로드 |
| `../brand guide/Line Icon/png/line-168.png` | 업로드 |
| `../brand guide/Line Icon/png/line-169.png` | 업그레이드 |
| `../brand guide/Line Icon/png/line-170.png` | 검색 |
| `../brand guide/Line Icon/png/line-171.png` | Good |
| `../brand guide/Line Icon/png/line-172.png` | Bad |
| `../brand guide/Line Icon/png/line-173.png` | 터치_01 |
| `../brand guide/Line Icon/png/line-174.png` | 터치_02 |
| `../brand guide/Line Icon/png/line-175.png` | 질문 |
| `../brand guide/Line Icon/png/line-176.png` | 대화 |
| `../brand guide/Line Icon/png/line-177.png` | 좋아요 |
| `../brand guide/Line Icon/png/line-178.png` | 스크랩 |
| `../brand guide/Line Icon/png/line-179.png` | 구독_01 |
| `../brand guide/Line Icon/png/line-180.png` | 구독_02 |
| `../brand guide/Line Icon/png/line-181.png` | 배송 |
| `../brand guide/Line Icon/png/line-182.png` | 분석 |
| `../brand guide/Line Icon/png/line-183.png` | 대화금지 |
| `../brand guide/Line Icon/png/line-184.png` | 체온 측정_01 |
| `../brand guide/Line Icon/png/line-185.png` | 체온 측정_02 |
| `../brand guide/Line Icon/png/line-186.png` | 방역 완료_01 |
| `../brand guide/Line Icon/png/line-187.png` | 방역 완료_02 |
| `../brand guide/Line Icon/png/line-188.png` | 마스크 착용_01 |
| `../brand guide/Line Icon/png/line-189.png` | 마스크 착용_02 |
| `../brand guide/Line Icon/png/line-190.png` | 비대면 상담 |

## 13) Life style

> 용도: 업종·생활 카테고리

| 파일 | 한글명 |
|---|---|
| `../brand guide/Line Icon/png/line-191.png` | Bakery |
| `../brand guide/Line Icon/png/line-192.png` | Food_01 |
| `../brand guide/Line Icon/png/line-193.png` | Food_02 |
| `../brand guide/Line Icon/png/line-194.png` | Cafe |
| `../brand guide/Line Icon/png/line-195.png` | Restaurant |
| `../brand guide/Line Icon/png/line-196.png` | Theme Park |
| `../brand guide/Line Icon/png/line-197.png` | Beauty_01 |
| `../brand guide/Line Icon/png/line-198.png` | Beauty_02 |
| `../brand guide/Line Icon/png/line-199.png` | Fashion_01 |
| `../brand guide/Line Icon/png/line-200.png` | Fashion_02 |
| `../brand guide/Line Icon/png/line-201.png` | Fashion_03 |
| `../brand guide/Line Icon/png/line-202.png` | Sports_01 |
| `../brand guide/Line Icon/png/line-203.png` | Sports_02 |
| `../brand guide/Line Icon/png/line-204.png` | Education |
| `../brand guide/Line Icon/png/line-205.png` | Shopping |
| `../brand guide/Line Icon/png/line-206.png` | Trip |
| `../brand guide/Line Icon/png/line-207.png` | Finance |
| `../brand guide/Line Icon/png/line-208.png` | Pet_01 |
| `../brand guide/Line Icon/png/line-209.png` | Pet_02 |
| `../brand guide/Line Icon/png/line-210.png` | Plant |

---

# 2D 아이콘

> 원본: `../brand guide/2D Icon/2D_Icon.pdf` (1p, 벡터)
> 추출본: `../brand guide/2D Icon/png/` — **10개, 투명 PNG**
> 규정: [brand.md](brand.md) 6.2 (8.3~8.5)

원본은 다크 배경 슬라이드 한 장에 10개가 격자로 배치돼 있었다. 카드 배경을 제거해 투명 PNG로 추출했다.
플랫 기반 + 입체감이 특징이며, 라인 아이콘과 달리 **컬러가 살아 있다.**

| 파일 | 이름 | 한글명 |
|---|---|---|
| `../brand guide/2D Icon/png/2d-01.png` | Point | 포인트 |
| `../brand guide/2D Icon/png/2d-02.png` | Media | 미디어·영상 |
| `../brand guide/2D Icon/png/2d-03.png` | Calendar | 캘린더·일정 |
| `../brand guide/2D Icon/png/2d-04.png` | Wallet | 지갑·결제 |
| `../brand guide/2D Icon/png/2d-05.png` | Coupon | 쿠폰 |
| `../brand guide/2D Icon/png/2d-06.png` | Manual | 이용안내서 |
| `../brand guide/2D Icon/png/2d-07.png` | Key | 열쇠·보안 |
| `../brand guide/2D Icon/png/2d-08.png` | Bell | 알림 |
| `../brand guide/2D Icon/png/2d-09.png` | Flag | 깃발·이벤트 |
| `../brand guide/2D Icon/png/2d-10.png` | Camera | 카메라·촬영 |

> **규정 문구와 실물이 다르다 — 2026-09-17 BX 확인 완료.** brand.md 6.2는 2D 아이콘을
> «오렌지·핑크 컬러로 생동감 표현»으로 적고 있지만, 실제 에셋 10개는 전부 **B Blue 계열**이고
> 오렌지·핑크 버전은 없다. **B Blue 버전을 그대로 등재해 쓴다** — brand.md 6.2 문구도 실물에 맞게 고쳤다.

> 10개뿐이라 커버리지가 좁다. 6.2가 말하는 «확장형»(메인 아이콘 중심에 연관 오브젝트 배치)은 에셋에 없다.
