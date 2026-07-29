"""
scan-pkgs.py — 扫描所有 packages 给 generate index.md 内容用
"""
import json
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')

def describe_pkg(pkg_dir):
    pj = pkg_dir / 'package.json'
    if not pj.exists():
        return {'name': pkg_dir.name, 'desc': '-'}
    try:
        d = json.loads(pj.read_text())
    except Exception:
        return {'name': pkg_dir.name, 'desc': '-'}
    return {
        'name': d.get('name', pkg_dir.name),
        'version': d.get('version', '0.0.0'),
        'desc': (d.get('description') or '').strip() or '-',
        'scripts': list(d.get('scripts', {}).keys())[:5],
    }

all_pkgs = []
for root in [ROOT / 'packages', ROOT / 'internal', ROOT / 'apps', ROOT / 'scripts']:
    if not root.exists():
        continue
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith('.'):
            continue
        if (d / 'package.json').exists():
            all_pkgs.append(d)

print(f'PACKAGES_COUNT={len(all_pkgs)}')
print()

for pkg_dir in all_pkgs:
    meta = describe_pkg(pkg_dir)
    print('===' + '=' * 70)
    print(f'PKG={meta["name"]}')
    print(f'VER={meta["version"]}')
    print(f'DESC={meta["desc"]}')
    print(f'SCRIPTS={" | ".join(meta["scripts"])}')

    src = pkg_dir / 'src'
    SKIP = {'node_modules', 'dist', '__tests__'}

    def walk(d, prefix, depth, max_d):
        if depth > max_d:
            return
        try:
            entries = sorted([x for x in d.iterdir()
                              if not x.name.startswith('.') and x.name not in SKIP],
                             key=lambda x: (0 if x.is_dir() else 1, x.name.lower()))
        except Exception:
            return
        dirs = [e for e in entries if e.is_dir()][:10]
        for e in dirs:
            print(f'TREE={prefix}{e.name}/')
            walk(e, prefix + '  ', depth + 1, max_d)
        if depth == 0:
            files = [e for e in entries if e.is_file()][:10]
            for e in files:
                print(f'TREE={prefix}{e.name}')

    base = src if src.exists() else pkg_dir
    max_d = 2 if src.exists() else 1
    walk(base, '', 0, max_d)
    print()
