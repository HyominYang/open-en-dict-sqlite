# open-en-dict-sqlite

[English Wiktionary](https://en.wiktionary.org) 데이터를 가공한 **오프라인 영영사전 SQLite 데이터베이스**.
네트워크·API 키 없이 단어로 정의·품사·발음(IPA)·예문을 조회할 수 있습니다.

## 데이터 출처와 라이선스

- **데이터**: English Wiktionary 공식 덤프([dumps.wikimedia.org](https://dumps.wikimedia.org)) 기반.
  원본 © Wiktionary 기여자, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
  이 저장소의 가공 데이터는 원본을 추출·재구조화한 2차 저작물이므로, 동일 조건에 따라
  **[CC BY-SA 4.0](LICENSE)** 으로 배포합니다.
- **빌더 코드**(`builder/`): **[MIT](LICENSE-code)**.

> 데이터(CC BY-SA)와 코드(MIT)의 라이선스는 분리되어 있습니다.

## 구성

```
open-en-dict-sqlite/
├── builder/        # Wiktionary 덤프 → SQLite 변환 스크립트 (MIT)
├── LICENSE         # 데이터: CC BY-SA 4.0
├── LICENSE-code    # 빌더 코드: MIT
└── (릴리스)         # 가공된 .sqlite 는 용량이 커 GitHub Releases 로 배포
```

## 스키마 (초안)

| 테이블 | 컬럼 |
|---|---|
| `entries` | `id`, `word`, `pos`(품사), `definition`(영어 정의), `ipa`(발음), `example`(예문) |

`word` 컬럼 인덱스로 조회. 한 단어에 여러 뜻이 있으면 여러 행으로 저장합니다.

## 상태

🚧 **초기 셋업.** 빌더 스크립트와 데이터는 추가 예정입니다.

## 작업 계획

1. English Wiktionary 덤프(또는 [kaikki.org](https://kaikki.org) 의 파싱본) 확보
2. `builder/` 에서 정의·품사·IPA·예문 추출 → SQLite 생성
3. 가공 데이터를 GitHub Releases 에 CC BY-SA 4.0 으로 공개
