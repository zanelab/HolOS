#!/usr/bin/env python3
"""Apply LLM translations to .trellis/spec files. (Built fresh, replacing older version)

Reads chunk-{01..10}.json + chunk-{01..10}.translations.json (built from
translation dict). Walks examples and substitutes masked -> translated.
"""
import json
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_DIR = ROOT / '.trellis' / 'spec'
CORPUS_DIR = Path('/opt/data/translation-corpus')

files_changed = 0
total_subs = 0
skipped_no_match = 0

for chunk_path in sorted(CORPUS_DIR.glob('chunk-*.json')):
    if chunk_path.name.endswith('.translations.json'):
        continue
    chunk_num = chunk_path.stem  # 'chunk-01'
    trans_path = CORPUS_DIR / f'{chunk_num}.translations.json'
    if not trans_path.exists():
        continue

    entries = json.loads(chunk_path.read_text())
    translations = {t['id']: t['translated_masked'] for t in json.loads(trans_path.read_text())}

    for entry in entries:
        eid = entry['id']
        translated = translations.get(eid, entry['masked'])
        if translated == entry['masked']:
            continue
        masked = entry['masked']
        for example in entry.get('examples', []):
            if ':' not in example:
                continue
            rel_path = example.rsplit(':', 1)[0]
            file_path = ROOT / rel_path
            if not file_path.exists():
                skipped_no_match += 1
                continue
            text = file_path.read_text()
            if translated in text:
                continue
            if masked not in text:
                skipped_no_match += 1
                continue
            new_text = text.replace(masked, translated, 1)
            file_path.write_text(new_text)
            files_changed += 1
            total_subs += 1

print(f'Files changed: {files_changed}')
print(f'Total substitutions: {total_subs}')
print(f'Skipped (no match): {skipped_no_match}')
