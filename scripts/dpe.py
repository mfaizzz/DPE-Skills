#!/usr/bin/env python3
"""DPE Skills: local catalogue search, distribution checks and Codex entry install."""
from __future__ import annotations
import argparse
import collections
import datetime
import json
import re
import shutil
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
TAGS = {
    'dpe-data-pipelines': 'snowflake adf azure fabric warehouse etl elt spark delta blob sql orchestration ingestion outbound',
    'dpe-data-architecture': 'snowflake warehouse schema dimensional modeling data architecture lineage',
    'dpe-rigorous-code-review': 'pull request branch diff implementation compliance review',
}
STOP = set('a an and are as at be by can do for from how i in into is it me my of on or our please skills that the this to use we with you your'.split())

def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('missing YAML frontmatter')
    lines = match.group(1).splitlines()
    fields = {}
    for index, line in enumerate(lines):
        m = re.match(r'^(name|description):\s*(.*)$', line)
        if not m:
            continue
        key, value = m.groups()
        if value in ('|', '>', '|-', '>-'):
            block = []
            for following in lines[index + 1:]:
                if following and not following[0].isspace():
                    break
                block.append(following.strip())
            value = ' '.join(block)
        elif value[:1] in ('"', "'") and value[-1:] == value[:1]:
            value = value[1:-1]
        fields[key] = value.strip()
    return fields

def catalogue(root: Path) -> list[dict]:
    rows = []
    for path in sorted((root / 'skills').glob('*/SKILL.md')):
        meta = frontmatter(path)
        rows.append({'id': path.parent.name, 'name': meta.get('name', ''),
                     'description': meta.get('description', ''), 'path': path.relative_to(root).as_posix()})
    return rows

def tokens(text: str) -> set[str]:
    words = re.findall(r'[a-z0-9]+', text.lower())
    return {w[:-1] if len(w) > 4 and w.endswith('s') else w for w in words if w not in STOP}

def search(root: Path, query: str, limit: int = 5) -> dict:
    rows = catalogue(root)
    aliases = json.loads((root / 'skills/aliases.json').read_text()).get('aliases', {})
    exact = aliases.get(query.lower().strip(), query.lower().strip())
    terms = tokens(query)
    scored = []
    # Rare matching terms discriminate better than generic words such as "code".
    frequencies = collections.Counter(t for row in rows for t in tokens(row['description'] + ' ' + row['id']))
    for row in rows:
        names = tokens(row['id'])
        description = tokens(row['description'] + ' ' + TAGS.get(row['id'], ''))
        score = sum((6 if t in names else 1.5) * (1 + 4 / (1 + frequencies[t]))
                    for t in terms if t in names or t in description)
        if row['id'] == 'dpe-data-pipelines' and re.search(r'\b(snowflake|adf|fabric|etl|elt)\b', query.lower()):
            score += 12
        if row['id'] == 'dpe-rigorous-code-review' and re.search(r'\b(pull request|pr|branch diff)\b', query.lower()):
            score += 12
        if row['id'] == exact:
            score += 10000
        row = dict(row, score=round(score, 3))
        if score > 0:
            scored.append(row)
    scored.sort(key=lambda x: (-x['score'], x['id']))
    ids = {r['id'] for r in rows}
    def available(items): return [x for x in items if x in ids]
    text = query.lower()
    complements = []
    if re.search(r'\b(e2e|end.to.end|migration|cutover|deployment readiness)\b', text):
        complements += ['dpe-e2e-review']
    if re.search(r'\b(doc|docs|documentation|write|writing|prose|copywriting|confluence|readme)\b', text):
        complements += ['dpe-quality-copywriting']
    if re.search(r'\b(comment|comments)\b', text): complements += ['dpe-quality-code']
    if re.search(r'\b(ui|interface|website|frontend|landing.page|responsive)\b', text):
        complements += ['dpe-quality-core', 'dpe-quality-ui', 'dpe-quality-human']
    if re.search(r'\b(mobile|responsive)\b', text): complements += ['dpe-quality-layoutmobile']
    return {'query': query, 'primary': scored[0]['id'] if scored else None,
            'matches': scored[:limit], 'complements': available(list(dict.fromkeys(complements))),
            'shared_gate': 'references/dpe/quality-gate.md',
            'note': 'Candidates only: read descriptions and select the smallest relevant set. No files changed or external services called.'}

def validate(root: Path) -> dict:
    errors = []
    try:
        rows = catalogue(root)
    except (OSError, ValueError) as exc:
        return {'status': 'FAIL', 'errors': [str(exc)]}
    if not rows: errors.append('No library skills found')
    ids = {r['id'] for r in rows}
    for row in rows:
        if row['name'] != row['id']: errors.append(f"{row['path']}: name differs from directory")
        if not re.fullmatch(r'[a-z0-9-]{1,64}', row['name']): errors.append(f"{row['path']}: invalid skill name")
        if not row['description']: errors.append(f"{row['path']}: missing description")
    for name in ['SKILL.md', 'README.md', 'LICENSE', 'docs/THIRD_PARTY_NOTICES.md',
                 'docs/third-party-licenses/base-library-MIT.txt', 'docs/third-party-licenses/anti-slop-MIT.txt',
                 'references/dpe/working-contract.md', 'references/dpe/e2e-review.md', 'references/dpe/quality-gate.md']:
        if not (root / name).is_file(): errors.append(f'Missing {name}')
    for path in (root / 'skills').glob('*.json'):
        try: json.loads(path.read_text())
        except (ValueError, OSError): errors.append(f'Invalid JSON: {path.relative_to(root)}')
    saved_catalogue = root / 'skills/catalog.json'
    if not saved_catalogue.is_file():
        errors.append('Missing skills/catalog.json; rebuild with the catalog command')
    else:
        try:
            if json.loads(saved_catalogue.read_text()) != rows:
                errors.append('Stale skills/catalog.json; rebuild with the catalog command')
        except ValueError:
            errors.append('Invalid skills/catalog.json')
    aliases = json.loads((root / 'skills/aliases.json').read_text()).get('aliases', {})
    for alias, target in aliases.items():
        if target not in ids: errors.append(f'Alias {alias} -> missing {target}')
    # Original source/copyright identifiers are required attribution, never active branding.
    for path in root.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts: continue
        rel = path.relative_to(root).as_posix()
        if re.search(r'bo[s]{1,2}ku', rel, re.I): errors.append(f'Legacy brand in active path: {rel}')
        legal = (rel.startswith('docs/third-party-licenses/') or rel in ['docs/THIRD_PARTY_NOTICES.md', 'docs/SOURCE_MANIFEST.json', 'docs/third-party.md']
                 or bool(re.search(r'(^|[/_-])(licen[cs]e|notice)([._/-]|$)', rel, re.I)))
        if legal: continue
        try: content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        # Spell the search pattern as pieces so this validator itself is not branded.
        old_brand = 'bo' + 'ss' + 'ku' + '|bo' + 's' + 'ku'
        if re.search(old_brand, content, re.I): errors.append(f'Legacy brand in active text: {rel}')
    return {'status': 'PASS' if not errors else 'FAIL', 'library_skills': len(rows),
            'entry_points': 1, 'errors': errors,
            'limits': 'Structural/routing checks only; not an audit or runtime validation of every third-party workflow.'}

def install(root: Path, destination: Path) -> dict:
    result = validate(root)
    if result['status'] != 'PASS': raise ValueError('Distribution validation failed; run validate first')
    destination = destination.expanduser().resolve()
    if destination == root.resolve() or root.resolve() in destination.parents:
        raise ValueError('Install destination must be outside the library checkout')
    # Do not activate hooks, touch global entry files or copy the whole library into the skill catalogue.
    current = [destination / 'SKILL.md', destination / 'agents/openai.yaml', destination / 'references/library-root.txt']
    existing = [p for p in current if p.exists()]
    backup = None
    if existing:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = destination.parent.parent / 'skill-backups' / ('dpe-skills-' + stamp)
        for old in existing:
            target = backup / old.relative_to(destination)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(old, target)
    for rel in ['SKILL.md', 'agents/openai.yaml']:
        target = destination / rel; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / rel, target)
    pointer = destination / 'references/library-root.txt'; pointer.parent.mkdir(parents=True, exist_ok=True)
    pointer.write_text(str(root.resolve()) + '\n')
    return {'status': 'INSTALLED', 'entry': str(destination), 'library': str(root.resolve()),
            'backup': str(backup) if backup else None, 'hooks_enabled': False}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    find = sub.add_parser('find'); find.add_argument('query'); find.add_argument('--limit', type=int, default=5)
    for command in ['validate', 'catalog', 'install']: sub.add_parser(command)
    for command in sub.choices.values(): command.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    sub.choices['install'].add_argument('--destination', type=Path, default=Path.home() / '.codex/skills/dpe-skills')
    args = parser.parse_args(argv)
    root = args.root.expanduser().resolve()
    try:
        if args.command == 'find': result = search(root, args.query, max(1, min(args.limit, 20)))
        elif args.command == 'validate': result = validate(root)
        elif args.command == 'catalog': result = catalogue(root)
        else: result = install(root, args.destination)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if isinstance(result, dict) and result.get('status') == 'FAIL' else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)})); return 1

if __name__ == '__main__':
    raise SystemExit(main())
