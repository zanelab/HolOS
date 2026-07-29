"""
generate-phantom-specs.py — 为没有真 package 对应的 spec dirs 生成占位 index.md
这样 51 个 spec dirs 都有内容。
"""
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_BASE = ROOT / '.trellis' / 'spec'

real_pkgs = set()
for root in [ROOT/'packages', ROOT/'internal', ROOT/'apps', ROOT/'scripts']:
    if not root.exists(): continue
    for d in root.iterdir():
        if d.is_dir() and (d/'package.json').exists():
            rel = str(d.relative_to(ROOT))
            if rel.startswith('internal/'): nm = rel[len('internal/'):]
            elif rel.startswith('apps/'): nm = rel[len('apps/'):]
            elif rel.startswith('packages/'): nm = rel[len('packages/'):]
            elif rel.startswith('scripts/'): nm = rel[len('scripts/'):]
            else: nm = rel
            real_pkgs.add(nm)

# Phantom dirs (in spec/ but no real package)
all_spec_dirs = sorted([d.name for d in SPEC_BASE.iterdir() if d.is_dir() and d.name not in {'guides'}])
phantom = [d for d in all_spec_dirs if d not in real_pkgs]
print(f'Phantom specs (no real package): {len(phantom)}')
for p in phantom:
    print(f'  {p}')

# Description templates (best-effort semantic)
PHANTOM_DESC = {
    '@core': 'Core workspace packages (`@vben-core/*`) — UI primitives shared across the vben monorepo. Combines base, typings, composables, design tokens, form/layout/menu/popup/shadcn/tabs UIs.',
    'access': 'Access control primitives — generateAccessible helpers, menu/permission checking, ACL primitives.',
    'common-ui': 'Common UI components — fallback pages, AuthenticationLoginExpiredModal, profile/about components (located in `_core/` of apps).',
    'design': 'Design tokens (Tailwind preset, color, spacing, typography) — base design language. Located at `@vben-core/design`.',
    'effects': 'Effects workspace packages (`@vben/effects/*`) — hooks, layouts, plugins, request, common-ui, access, mock backends.',
    'form-ui': 'Form UI primitives — input wrappers, validators, integration with adapters (antd/tdesign/naive/ele).',
    'layout-ui': 'Layout UI primitives — `VbenLayout`, `LayoutSidebar`, `LayoutHeader`, `LayoutTabbar`, `LayoutContent`, `LayoutFooter`.',
    'menu-ui': 'Menu UI primitives — sidebar menu items, breadcrumb, tab chrome.',
    'popup-ui': 'Popup UI primitives — modal, drawer, dropdown, select, popover wrappers.',
    'shadcn-ui': 'shadcn-vue primitives — buttons, inputs, dialogs. Wrapped as Vben-prefixed components.',
    'tabs-ui': 'Tab UI primitives — draggable tab chrome, context menu, refresh, close.',
    'base': 'Base workspace (`@vben-core/base`) — global types, shared typings, helper interfaces. Other packages depend on `base`.',
    'shared': 'Shared workspace (`@vben-core/shared`) — runtime constants (ELEMENT_ID_*), bootstrap tokens, generic helpers.',
    'typings': 'Typings workspace (`@vben-core/typings`) — generic TS types (ComponentRecord, Recordable, etc).',
    'composables': 'Composables workspace (`@vben-core/composables`) — `useScroll`, `useScrollbar`, etc.',
    'design-tokens': 'Design tokens (legacy alias — see `design/`).',
    'design-ui': 'Design UI components (legacy alias — see `design/`).',
    'preferences': 'Preferences workspace (`@vben-core/preferences`) — typed configuration, `defineOverridesPreferences`, default preferences.',
    'plugins': 'Plugins workspace (`@vben/plugins`) — vite plugin adapters (vue, html, mock, etc).',
    'request': 'Request workspace (`@vben/request`) — `requestClient`, axios wrapper, SSO helpers.',
    'commitlint-config': 'commitlint shared config — base rules + scope enum mapping.',
    'lint-configs': 'Lint shared configs — parent dir of oxlint/eslint/stylelint/oxfmt config packages.',
    'eslint-config': 'ESLint flat config for vben apps.',
    'stylelint-config': 'stylelint config for vben apps (Vue + CSS).',
    'oxlint-config': 'OxLint config (Rust-based linter, fast replacement for ESLint).',
    'oxlint-config': 'OxLint config (Rust-based linter, fast replacement for ESLint).',
    'oxfmt-config': 'OxFmt config (Rust-based formatter, fast replacement for Prettier).',
    'oxlint-config': 'OxLint config (Rust-based linter).',
    'stylelint-config': 'stylelint config (Vue + CSS).',
    'esaccess': 'alias for `@vben/access` (legacy alias).',
    'common': 'common alias — see `common-ui/`.',
    'layouts': 'Layouts workspace (`@vben/layouts`) — BasicLayout, AuthenticationLayout, IFrameView.',
    'icons': 'Icons workspace (`@vben/icons`) — iconify + svg icons, `Svg*Icon` exports. Used in IconifyIcon component.',
    'styles': 'Styles workspace (`@vben/styles`) — design CSS per UI framework (antd/ele/naive/antdv-next) and global',
    'icons': 'Icons workspace (`@vben/icons`) — `Svg*Icon` exports.',
    'uikit': 'UI-Kit alias — see `@core/`.',
    'ui-kit': 'UI-Kit alias — see `@core/`.',
    'system': 'System mock API — see `backend-mock/`.',
}

DEFAULT_DESC = 'Placeholder package in vben monorepo. Real package does not exist yet — this spec is here so AI agents know the conventions for this name. If a package is created later, replace this placeholder with real conventions.'

# Determine if it's web-app or lib
def is_kind(n):
    if n.startswith('@vben/web-') or n == 'apps/web-holos' or 'web-' in n: return 'app'
    if n in ('backend-mock', 'docs', 'playground'): return 'mfe-mock' if n == 'backend-mock' else 'doc'
    return 'lib'

template = '''# {name}

> vben monorepo package spec — placeholder until the package is created.

## Status

⚠️ **Placeholder spec.** No actual package named `{name}` exists in the workspace yet. This file was auto-generated by Trellis init to ensure AI agents don't hallucinate conventions for unknown packages.

When the package is added:
1. Move this file from placeholder to real content
2. Fill `directory-structure.md`, `quality-guidelines.md`, etc.
3. Update `task.json` for any related bootstrap subtasks

## Conventions (inherited from monorepo)

> {desc}

- **Language**: All documentation in **English** (some user-facing docs may be Chinese)
- **TypeScript strict mode** is required
- **Lint**: ESLint flat config + OxLint + Stylelint (auto on commit via lefthook)
- **Naming**:
  - Component files: `kebab-case.vue`
  - Composable files: `use-*.ts`
  - Utility files: `kebab-case.ts` or grouped in `utils/`/`helpers/`
- **Public API**: re-export from `src/index.ts` only — no deep imports
- **Workspace aliases**: `@vben/*` for packages, `@vben-core/*` for internal core, `@/*` for app-level, `#/*` for app-shared

## Forbidden

- ❌ Don't introduce new build configurations in this directory
- ❌ Don't reimplement what `@vben/utils` / `@vben/constants` / `@vben/hooks` already provide
- ❌ Don't bypass `src/index.ts` with deep imports
- ❌ Don't add dependencies without bumping this spec's `dependencies` list

## Related

- See `.. /../spec/guides/` for cross-package conventions
- See `.trellis/workflow.md` for the development workflow
- See `.trellis/spec/web-holos/` for the customized HolOS app spec (built on `@vben/web-tdesign`)
'''

generated = 0
for spec_name in phantom:
    spec_dir = SPEC_BASE / spec_name
    if not spec_dir.exists():
        continue
    desc = PHANTOM_DESC.get(spec_name, DEFAULT_DESC)
    md = template.replace('{name}', spec_name).replace('{desc}', desc)
    # Write to both frontend and backend (or single if kind is app-only)
    aspects = ['frontend', 'backend'] if is_kind(spec_name) == 'lib' else ['frontend']
    for aspect in aspects:
        aspect_dir = spec_dir / aspect
        if not aspect_dir.exists():
            aspect_dir.mkdir(parents=True, exist_ok=True)
        idx = aspect_dir / 'index.md'
        try:
            existing = idx.read_text() if idx.exists() else ''
        except: existing = ''
        # Skip if already written with real content
        if existing and 'Best practices for' not in existing and 'To fill' not in existing and 'No actual package' not in existing and len(existing) > 600:
            # has real content — skip
            pass
        else:
            idx.write_text(md)
            generated += 1

print(f'\\nGenerated {generated} phantom index.md files for {len(phantom)} spec dirs (some may already exist)')
