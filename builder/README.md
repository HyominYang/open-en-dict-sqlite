# builder

English Wiktionary 추출 데이터(wiktextract)를 영영사전 SQLite 로 변환한다.

## 입력 데이터
[kaikki.org](https://kaikki.org/dictionary/English/) 의 wiktextract **JSONL** (한 줄에 객체 1개).
- English 추출본(권장), 또는 전체 `raw-wiktextract-data`(약 22GB / gz 2.6GB) — 후자는 `lang_code=="en"` 으로 자동 필터.

## 사용법
```
python3 build.py <input.jsonl> [output.sqlite]
```
- 표준 라이브러리만 사용(`json`, `sqlite3`) — **설치할 의존성 없음.** Python 3.8+.
- 출력 기본값: `open-en-dict.sqlite`

## 출력 스키마
```
entries(id, word, pos, definition, ipa, example)   -- word 인덱스
```
- 한 단어의 각 뜻(sense)마다 한 행 (다의어 = 여러 행)
- `definition` = sense 의 glosses, `ipa` = 단어 단위 첫 발음, `example` = sense 의 첫 예문

## 라이선스
- 코드: **MIT** (`../LICENSE-code`)
- 생성 데이터: **CC BY-SA 4.0** — 원본 Wiktionary 의 동일 조건 상속 (`../LICENSE`)
