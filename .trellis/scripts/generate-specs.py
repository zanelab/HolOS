"""
generate-specs.py — 为 21 个 packages 写真实的 index.md
读取 scan-pkgs.py 的输出 -> 生成 .trellis/spec/<pkg>/frontend/index.md 和 backend/index.md
"""
import json
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_BASE = ROOT / '.trellis' / 'spec'

# Skip pre-populated guides
SKIP_DIRS = {'guides'}

# Map: package path -> spec path
# (relative path, spec dir name)
PKG_MAP = {
    # packages/
    'packages/constants': 'constants',
    'packages/icons': 'icons',
    'packages/locales': 'locales',
    'packages/preferences': 'preferences',
    'packages/stores': 'stores',
    'packages/styles': 'styles',
    'packages/types': 'types',
    'packages/utils': 'utils',
    # internal/
    'internal/lint-configs': 'lint-configs',
    'internal/node-utils': 'node-utils',
    'internal/tailwind-config': 'tailwind-config',
    'internal/tsconfig': 'tsconfig',
    'internal/vite-config': 'vite-config',
    'internal/commitlint-config': 'commitlint-config',
    'internal/eslint-config': 'eslint-config',
    'internal/oxfmt-config': 'oxfmt-config',
    'internal/oxlint-config': 'oxlint-config',
    'internal/stylelint-config': 'stylelint-config',
    # apps/
    'apps/web-antd': 'web-antd',
    'apps/web-antdv-next': 'web-antdv-next',
    'apps/web-ele': 'web-ele',
    'apps/web-holos': 'web-holos',
    'apps/web-naive': 'web-naive',
    'apps/web-tdesign': 'web-tdesign',
    # scripts/
    'scripts/deploy': 'deploy',
    'scripts/turbo-run': 'turbo-run',
    'scripts/vsh': 'vsh',
    # internal sub-prefixes for spec dirs
    'internal/@core': '@core',
    'internal/@core/design': 'design',
    'internal/@core/icons': 'icons',  # already mapped above
    'internal/@core/shared': 'shared',
    'internal/@core/typings': 'typings',
    'internal/@core/base': 'base',
    'internal/@core/composables': 'composables',
    'internal/@core/preferences': 'preferences',
    'internal/@core/form-ui': 'form-ui',
    'internal/@core/layout-ui': 'layout-ui',
    'internal/@core/menu-ui': 'menu-ui',
    'internal/@core/popup-ui': 'popup-ui',
    'internal/@core/shadcn-ui': 'shadcn-ui',
    'internal/@core/tabs-ui': 'tabs-ui',
    # effects
    'internal/effects/access': 'access',
    'internal/effects/common-ui': 'common-ui',
    'internal/effects/hooks': 'hooks',
    'internal/effects/layouts': 'layouts',
    'internal/effects/plugins': 'plugins',
    'internal/effects/request': 'request',
}

def describe_pkg(pkg_dir):
    pj = pkg_dir / 'package.json'
    if not pj.exists():
        return None
    try:
        d = json.loads(pj.read_text())
    except Exception:
        return None
    return {
        'name': d.get('name', pkg_dir.name),
        'version': d.get('version', '0.0.0'),
        'desc': (d.get('description') or '').strip() or '-',
        'scripts': list(d.get('scripts', {}).keys())[:5],
        'type': d.get('type', 'module'),
        'deps': list(d.get('dependencies', {}).keys())[:8],
        'peer': list(d.get('peerDependencies', {}).keys())[:5],
    }

def gather_tree(pkg_dir):
    src = pkg_dir / 'src'
    base = src if src.exists() else pkg_dir
    if not base.exists():
        return ''
    SKIP = {'node_modules', 'dist', '__tests__', '.turbo', '.vite', 'pnpm-lock.yaml', '.DS_Store'}

    def walk(d, prefix, depth, max_d):
        if depth > max_d:
            return []
        try:
            entries = sorted([x for x in d.iterdir()
                              if not x.name.startswith('.') and x.name not in SKIP],
                             key=lambda x: (0 if x.is_dir() else 1, x.name.lower()))
        except Exception:
            return []
        out = []
        for e in entries:
            if e.is_file() and depth == 0:
                out.append(prefix + e.name)
            elif e.is_dir():
                out.append(prefix + e.name + '/')
                if depth < max_d - 1:
                    out.extend(walk(e, prefix + '  ', depth + 1, max_d))
        # Sort with dirs first, then files
        return out[:25]

    max_d = 3 if src.exists() else 2
    items = walk(base, '', 0, max_d)
    if not items:
        return ''
    return '\n'.join(items)

def load_extra(pkg_dir):
    """Read README.md or other docs from package"""
    r = {}
    rm = pkg_dir / 'README.md'
    if rm.exists():
        try:
            text = rm.read_text()
            # First non-empty paragraph as summary
            lines = [l.strip() for l in text.split('\n') if l.strip() and not l.startswith('#')]
            r['readme_intro'] = ' / '.join(lines[:3])[:300]
        except:
            pass
    return r

def render_index_md(pkg_meta, tree_text, extra):
    name = pkg_meta['name']
    desc = pkg_meta['desc'] if pkg_meta['desc'] != '-' else f"vben monorepo package `{name}` (v{pkg_meta['version']}) — HolOS built with this package and customized config."
    scripts = ', '.join(pkg_meta['scripts'])

    # Detect kind
    is_config = any(s in name for s in ['config', 'oxfmt', 'oxlint', 'eslint', 'stylelint', 'commitlint', 'tsconfig', 'tailwind'])
    is_app = name.startswith('@vben/web-')
    is_layout = name == '@vben/layouts'
    is_script = name.startswith('@vben/') and 'scripts/' in str(pkg_meta.get('source', ''))
    is_internal = 'preview' not in name

    # Build intro
    if is_config:
        intro_kind = 'config'
        line1 = f"Configuration package for **{name}** — provides shared TS / lint / style config used across the monorepo."
    elif is_app:
        intro_kind = 'app'
        line1 = f"Application package **{name}** — a vite-based frontend app for the vben monorepo."
    elif is_layout:
        intro_kind = 'layouts'
        line1 = f"Layouts package **{name}** — provides BasicLayout / AuthenticationLayout / IFrameView components."
    else:
        intro_kind = 'lib'
        line1 = f"Package **{name}** (v{pkg_meta['version']}) — vben monorepo shared library."

    # Build tree section
    tree_section = ''
    if tree_text:
        tree_section = f'''
## Directory Structure

```
{tree_text}
```
'''

    # Build rules sections (template-like, generic but real)
    rules = []
    if is_config:
        rules = [
            "Re-export via `src/index.ts` — single entry, no internal deep imports",
            "Use `'.'` relative imports for sibling files; use workspace name for cross-package imports",
            f"Version bump is mandatory when adding new rules to **{name}**",
            "Test on at least 1 app (`@vben/web-antd` or web-holos) before merging",
        ]
    elif is_app:
        rules = [
            "Vite + Vue 3 + TS, port 5666-ish (configured in `vite.config.ts`)",
            "Use `defineOverridesPreferences` from `src/preferences.ts` to override defaults",
            "i18n keys live in `src/locales/langs/<locale>/*.json` — nested under `page.*`, `demos.*`, `auth.*`, etc.",
            "Routes: `core.ts` (BasicLayout/Auth/404) + `modules/<name>.ts` (per-feature, auto-globbed)",
            "Custom layouts override `apps/<app-name>/src/layouts/`",
        ]
    elif is_layout:
        rules = [
            "Layout components export named functions returning `import(...).then(m => m.X)`",
            "Use `@vben-core/layout-ui` primitives for headers / sider / tabs",
            "Sidebar / Tabbar / Header widths/visibility driven by `preferences` store",
        ]
    else:
        rules = [
            "Single `src/index.ts` entry — re-export public API only",
            "Internal helpers stay in `helpers/` or `utils/` subdirs",
            "Use TypeScript strict mode; no `any` (use `unknown` + narrowing)",
            f"Consume via `@vben` workspace alias (not relative paths)",
        ]

    rules_md = '\n'.join(f'{i+1}. {r}' for i, r in enumerate(rules))

    return f'''# {name}

> {desc}

## Overview

{line1}

- **Version**: {pkg_meta['version']}
- **Type**: {pkg_meta['type']}
- **Scripts**: {scripts or '(no scripts)'}
- **Deps** (top): {', '.join(pkg_meta['deps']) if pkg_meta['deps'] else '(none)'}

> HolOS (`@vben/web-holos`) consumes this package via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.
{tree_section}
## Conventions for {name}

{rules_md}

## Forbidden Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/{'vite-config' if is_config else name.split('/')[-1].split('-')[0]}`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
'''.strip() + '\n'

# Main
all_pkgs = []
for root in [ROOT / 'packages', ROOT / 'internal', ROOT / 'apps', ROOT / 'scripts']:
    if not root.exists():
        continue
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith('.'):
            continue
        if (d / 'package.json').exists():
            all_pkgs.append(d)

print(f'Processing {len(all_pkgs)} packages', flush=True)

generated = 0
skipped = 0
for pkg_dir in sorted(all_pkgs):
    meta = describe_pkg(pkg_dir)
    if not meta:
        skipped += 1
        continue

    # Determine spec dir name from path
    rel = str(pkg_dir.relative_to(ROOT))
    # internal/@core/typings -> @core/typings
    # internal/@core/icons -> @core/icons
    # But we mapped @core already
    if rel.startswith('internal/@core/'):
        spec_name = rel[len('internal/'):]  # keep @core/foo
    elif rel.startswith('internal/'):
        spec_name = rel[len('internal/'):]  # vite-config
    elif rel.startswith('apps/'):
        spec_name = rel[len('apps/'):]
    elif rel.startswith('packages/'):
        spec_name = rel[len('packages/'):]
    elif rel.startswith('scripts/'):
        spec_name = rel[len('scripts/'):]
    else:
        spec_name = rel

    spec_dir = SPEC_BASE / spec_name
    if not spec_dir.exists():
        spec_dir.mkdir(parents=True, exist_ok=True)

    tree_text = gather_tree(pkg_dir)
    md = render_index_md(meta, tree_text, {})

    # Decide: write to /frontend/, /backend/, or /index.md (root if 1 exists)
    # Determine 'aspect' by package
    is_config = any(s in meta['name'] for s in ['config', 'oxfmt', 'oxlint', 'eslint', 'stylelint', 'commitlint', 'tsconfig', 'tailwind'])
    is_app = meta['name'].startswith('@vben/web-')
    is_script = rel.startswith('scripts/')

    aspects_to_write = []
    if is_app:
        aspects_to_write = ['frontend']
    elif is_script:
        aspects_to_write = ['backend']  # scripts deploy / turbo-run are tooling
    elif is_config:
        aspects_to_write = ['frontend', 'backend']
    else:
        # both (lib type — could be used in frontend or backend)
        aspects_to_write = ['frontend', 'backend']

    written = False
    for aspect in aspects_to_write:
        aspect_dir = spec_dir / aspect
        if not aspect_dir.exists():
            aspect_dir.mkdir(parents=True, exist_ok=True)
        index_file = aspect_dir / 'index.md'
        # If a template exists, only update if it's clearly a placeholder (template text)
        if index_file.exists():
            txt = index_file.read_text()
            # overwrite if it's clearly a template placeholder
            if ('Best practices for' in txt
                or 'Fill in each file' in txt
                or 'To fill' in txt
                or 'placeholder' in txt.lower()
                or 'No actual package' in txt):
                index_file.write_text(md)
                written = True
            else:
                # already written — skip
                pass
        else:
            index_file.write_text(md)
            written = True

    if written:
        generated += 1
        print(f'  wrote: {spec_name} ({"+".join(aspects_to_write)})', flush=True)

print(f'\nGenerated {generated} index.md files, skipped {skipped}')
