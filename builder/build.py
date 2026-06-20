#!/usr/bin/env python3
"""kaikki.org(wiktextract) JSONL → 영영+영한 사전 SQLite.

사용법:
    python3 build.py <input.jsonl> [output.sqlite]

입력: kaikki.org 의 English wiktextract JSONL.
      전체 raw-wiktextract-data(다국어)를 줘도 lang_code=="en" 만 추린다.
출력: entries(word, pos, definition, ipa, example, korean) — word 인덱스.
      - definition: 영어 정의(sense glosses)
      - korean   : Wiktionary translations 의 한국어 대역(단어 단위, 최대 6개 "; ")
      한 단어의 각 뜻(sense)마다 한 행. ipa·korean 은 단어 단위로 공유.

표준 라이브러리만 사용(json, sqlite3). Python 3.8+.
"""
import json
import sqlite3
import sys

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    word       TEXT NOT NULL,
    pos        TEXT,
    definition TEXT NOT NULL,
    ipa        TEXT,
    example    TEXT,
    korean     TEXT
);
"""


def first_ipa(entry):
    """sounds[] 에서 첫 IPA 표기를 찾는다."""
    for s in entry.get("sounds") or []:
        ipa = s.get("ipa")
        if ipa:
            return ipa
    return None


def korean_of(entry):
    """translations[] 에서 한국어 대역을 모은다(중복 제거, 최대 6개). 없으면 None.

    wiktextract 의 translations 항목은 {"code":"ko","word":"사과", ...} 형태.
    옛 데이터 호환으로 lang_code 도 함께 본다.
    """
    ko = []
    for t in entry.get("translations") or []:
        if t.get("code") == "ko" or t.get("lang_code") == "ko":
            w = t.get("word")
            if w and w not in ko:
                ko.append(w)
    return "; ".join(ko[:6]) if ko else None


def rows_from(entry):
    """wiktextract 엔트리 1개 → (word, pos, definition, ipa, example, korean) 행들."""
    word = entry.get("word")
    if not word:
        return
    pos = entry.get("pos")
    ipa = first_ipa(entry)
    korean = korean_of(entry)
    for sense in entry.get("senses") or []:
        glosses = sense.get("glosses") or sense.get("raw_glosses")
        if not glosses:
            continue
        # wiktextract glosses 는 [상위 범주, …, 구체 정의] 계층이라 마지막이 그
        # sense 의 실제 정의다. join 하면 상위("To move swiftly.")가 매 행
        # 반복되므로, 비어있지 않은 마지막 요소만 쓴다.
        definition = next((g for g in reversed(glosses) if g), "").strip()
        if not definition:
            continue
        example = None
        for ex in sense.get("examples") or []:
            text = ex.get("text")
            if text:
                example = text
                break
        yield (word, pos, definition, ipa, example, korean)


def main():
    if len(sys.argv) < 2:
        print("usage: python3 build.py <input.jsonl> [output.sqlite]", file=sys.stderr)
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "open-en-dict.sqlite"

    conn = sqlite3.connect(out)
    conn.executescript(SCHEMA)
    cur = conn.cursor()

    n_lines = n_rows = 0
    with open(inp, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n_lines += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            # 전체(다국어) wiktextract 를 입력으로 줬을 때 영어만 남긴다.
            lang = entry.get("lang_code")
            if lang and lang != "en":
                continue
            batch = list(rows_from(entry))
            if batch:
                cur.executemany(
                    "INSERT INTO entries(word, pos, definition, ipa, example, korean) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    batch,
                )
                n_rows += len(batch)
            if n_lines % 100_000 == 0:
                conn.commit()
                print(f"  {n_lines:,} lines -> {n_rows:,} rows", file=sys.stderr)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_entries_word ON entries(word)")
    conn.commit()
    conn.close()
    print(f"done: {n_lines:,} lines -> {n_rows:,} rows -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
