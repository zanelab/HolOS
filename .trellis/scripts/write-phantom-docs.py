#!/usr/bin/env python3
"""Write 2 sub-files (directory-structure + component-guidelines) for each phantom spec.

Real @vben/* phantom packages have been specified in vben v5.7.0 monorepo but
the actual package directories don't exist. We write best-guess docs that
match vben monorepo conventions.

Run:
  python3 .trellis/scripts/write-phantom-docs.py
"""
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')

# (spec_dir_name, kind, description, kind-aware notes)
PHANTOMS = [
    ('@core', 'phantom-core', '@vben-core/* shared UI primitives (combines all internal@core/* packages)'),
    ('access', 'phantom-access', '@vben/access — generateAccessible + ACL primitives (planned)'),
    ('base', 'phantom-base', '@vben-core/base — global types and shared interfaces (planned)'),
    ('common-ui', 'phantom-common-ui', '@vben/common-ui — fallback pages, profile/about/auth login (planned)'),
    ('composables', 'phantom-composables', '@vben-core/composables — useScroll, useScrollbar etc (planned)'),
    ('design', 'phantom-design', '@vben-core/design — design tokens (planned)'),
    ('form-ui', 'phantom-form-ui', '@vben-core/form-ui — form input wrappers + validators (planned)'),
    ('hooks', 'phantom-hooks', '@vben/hooks — custom hooks (planned)'),
    ('layout-ui', 'phantom-layout-ui', '@vben-core/layout-ui — VbenLayout primitives (planned)'),
    ('layouts', 'phantom-layouts', '@vben/layouts — BasicLayout / AuthenticationLayout (planned)'),
    ('menu-ui', 'phantom-menu-ui', '@vben-core/menu-ui — sidebar menu + breadcrumb (planned)'),
    ('plugins', 'phantom-plugins', '@vben/plugins — vite plugin adapters (planned)'),
    ('popup-ui', 'phantom-popup-ui', '@vben-core/popup-ui — modal/drawer/dropdown/popover (planned)'),
    ('request', 'phantom-request', '@vben/request — requestClient axios wrapper (planned)'),
    ('shared', 'phantom-shared', '@vben-core/shared — runtime constants (planned)'),
    ('shadcn-ui', 'phantom-shadcn-ui', '@vben-core/shadcn-ui — shadcn-vue primitives (planned)'),
    ('tabs-ui', 'phantom-tabs-ui', '@vben-core/tabs-ui — tab UI primitives (planned)'),
    ('typings', 'phantom-typings', '@vben-core/typings — generic TS types (planned)'),
]


def write_phantom(spec_dir_name, kind, desc):
    spec_dir = ROOT / '.trellis' / 'spec' / spec_dir_name / 'frontend'
    spec_dir.mkdir(parents=True, exist_ok=True)

    placeholder_banner = '> **PLACEHOLDER DOCS** — This package does not exist in the workspace at this time. The expected structure and patterns below are based on `vben v5.7.0` conventions. Replace these files with real content when the package is added.'

    (spec_dir / 'directory-structure.md').write_text(
        f'# {spec_dir_name} Directory Structure\n\n'
        f'**Expected package:** {desc}\n\n'
        f'{placeholder_banner}\n\n'
        '## Expected Tree\n\n'
        '```\n'
        f'@vben/{spec_dir_name.lstrip("@vben-").lstrip("@core/")}/\n'
        '├── package.json                # workspace name\n'
        '├── tsconfig.json\n'
        '└── src/\n'
        '    ├── index.ts                # public barrel\n'
        '    └── (one or more module files)\n'
        '```\n\n'
        '## Notes\n\n'
        '- This spec directory was auto-created during `bootstrap-guidelines` task\n'
        '- The expected structure follows `vben v5.7.0` conventions seen in actual packages (`@vben/utils`, `@vben/constants`, etc.)\n'
        '- See real packages for reference examples\n\n'
        '## Forbidden\n\n'
        '- Do not create the actual package directory in workspace unless the upstream vben team adds it\n'
        '- Do not import from `@vben/' + spec_dir_name.lstrip('@vben/').lstrip('@core/') + '` — it does not exist'
    )

    (spec_dir / 'component-guidelines.md').write_text(
        f'# {spec_dir_name} Component Guidelines\n\n'
        f'**Expected package:** {desc}\n\n'
        f'{placeholder_banner}\n\n'
        '## Expected Conventions\n\n'
        '- Vue 3 + TypeScript strict mode (when applicable)\n'
        '- Single barrel at `src/index.ts` (re-export public API)\n'
        '- Tree-shake friendly (named exports only)\n'
        '- Tests in `__tests__/` alongside source\n\n'
        '## Example (synthetic)\n\n'
        '```ts\n'
        '// src/index.ts\n'
        'export * from \'./helpers\';\n'
        'export { useXxx } from \'./use-xxx\';\n'
        '```\n\n'
        '## Forbidden\n\n'
        '- Do not implement against this placeholder before the real package exists\n'
        '- Do not deep-import from `@vben/' + spec_dir_name.lstrip('@vben/').lstrip('@core/') + '/internal/*` (package does not exist)\n'
        '- Do not add real source files under `internal/<phantom>/`'
    )


def main():
    written = 0
    for spec_name, kind, desc in PHANTOMS:
        try:
            write_phantom(spec_name, kind, desc)
            written += 1
        except Exception as e:
            print(f'  failed {spec_name}: {e}')

    print(f'wrote placeholder docs for {written} phantom specs')


if __name__ == '__main__':
    main()
