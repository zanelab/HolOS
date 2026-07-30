#!/usr/bin/env python3
"""Write 4 shared sub-files (hook / state / quality / type) for phantom specs.

For packages that don't exist in workspace (phantom specs), write best-guess
docs matching vben v5.7.0 conventions.

Run:
  python3 .trellis/scripts/write-phantom-4.py
"""
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')

PHANTOMS = [
    '@core', 'access', 'base', 'common-ui', 'composables', 'design',
    'form-ui', 'hooks', 'layout-ui', 'layouts', 'menu-ui', 'plugins',
    'popup-ui', 'request', 'shared', 'shadcn-ui', 'tabs-ui', 'typings',
]


def placeholder_banner():
    return (
        '> **PLACEHOLDER DOCS** - This package does not exist in the workspace at this time. '
        'Expected conventions are based on vben v5.7.0 monorepo. '
        'Replace these files with real content when the package is added.'
    )


def write_hook(spec_dir, name):
    (spec_dir / 'hook-guidelines.md').write_text(
        f'# {name} Custom Hooks\n\n'
        + placeholder_banner() + '\n\n'
        '## Expected Conventions\n\n'
        '- For Vue apps: composables go in src/composables/\n'
        '- Co-located hooks in src/views/<feature>/ for one-feature usage\n'
        '- Shared hooks in src/hooks/\n'
        '- For libs: package itself has no Vue hooks (consumed via Vue apps)\n\n'
        '## Example (synthetic)\n\n'
        '```ts\n'
        '// src/composables/use-x-resource.ts\n'
        'import { ref, shallowRef } from "vue";\n\n'
        'export function useXResource(loader: () => Promise<XData>) {\n'
        '  const data = shallowRef<XData>();\n'
        '  const loading = ref(false);\n'
        '  async function refresh() {\n'
        '    loading.value = true;\n'
        '    try { data.value = await loader(); }\n'
        '    finally { loading.value = false; }\n'
        '  }\n'
        '  return { data, loading, refresh };\n'
        '}\n'
        '```\n\n'
        '## Built-ins (always check first)\n\n'
        '| Concern | Hook | Source |\n'
        '|---|---|---|\n'
        '| App config | usePreferences() | @vben/preferences |\n'
        '| Pinia | useAccessStore / useUserStore / useAuthStore | @vben/stores |\n'
        '| i18n | useI18n() | vue-i18n |\n\n'
        '## Forbidden\n\n'
        '- Do not implement against this phantom package before it exists\n'
        '- Do not wrap usePreferences() in another composable\n'
        '- Do not put pure business logic in a hook (use src/utils/ instead)\n'
    )


def write_state(spec_dir, name):
    (spec_dir / 'state-management.md').write_text(
        f'# {name} State Management\n\n'
        + placeholder_banner() + '\n\n'
        '## Expected Decision Tree\n\n'
        '| Where state lives | Use |\n'
        '|---|---|\n'
        '| One component | ref() / reactive() |\n'
        '| Cross-page, persisted | preferences store (@vben/preferences) |\n'
        '| Cross-page, transient | Pinia store (@vben/stores) |\n'
        '| Server cache | API + useXResource pattern |\n\n'
        '## Example (synthetic)\n\n'
        '```ts\n'
        '// Apps: use Pinia store\n'
        'import { defineStore } from "pinia";\n'
        'export const useXStore = defineStore("x", () => {\n'
        '  const xList = ref<XItem[]>([]);\n'
        '  return { xList };\n'
        '});\n\n'
        '// Libs: stateless, callers handle state\n'
        'export function transformX(input: XInput): XOutput { /* pure */ }\n'
        '```\n\n'
        '## Forbidden\n\n'
        '- Do not persist auth tokens in localStorage (XSS risk)\n'
        '- Do not use Vuex (this monorepo uses Pinia)\n'
        '- Do not mutate preferences outside the store API\n'
    )


def write_quality(spec_dir, name):
    (spec_dir / 'quality-guidelines.md').write_text(
        f'# {name} Quality Guidelines\n\n'
        + placeholder_banner() + '\n\n'
        '## Expected Style\n\n'
        '- 4 spaces TS / Vue indent\n'
        '- Single quotes TS; double quotes HTML\n'
        '- No semicolons (OxFmt auto-format)\n'
        '- Max line length 120\n'
        '- Trailing newline required\n\n'
        '## Expected Naming\n\n'
        '| Thing | Convention |\n'
        '|---|---|\n'
        '| Vue page file | PascalCase.vue |\n'
        '| Component | kebab-case.vue |\n'
        '| Composable | useCamelCase |\n'
        '| Pinia store | useXxxStore |\n'
        '| Constant | UPPER_SNAKE_CASE |\n\n'
        '## Pre-commit Hooks\n\n'
        '- OxLint (fast)\n'
        '- OxFmt (formatter)\n'
        '- ESLint (rules OxLint misses)\n'
        '- Stylelint (CSS / Vue style)\n'
        '- Commitlint (feat(): / fix(): / chore():)\n\n'
        '## Forbidden\n\n'
        '- Do not use any\n'
        '- Do not add @ts-ignore without comment\n'
        '- Do not commit .env or secrets\n'
        '- Do not implement against this phantom package\n'
    )


def write_type(spec_dir, name):
    (spec_dir / 'type-safety.md').write_text(
        f'# {name} Type Safety\n\n'
        + placeholder_banner() + '\n\n'
        '## Expected Config\n\n'
        '- Apps: tsconfig.json extends @vben/tsconfig/web-app.json\n'
        '- Libs: tsconfig.json extends @vben/tsconfig/library.json\n'
        '- Strict mode ON (no implicit any, strict null checks)\n\n'
        '## Expected Patterns\n\n'
        '```ts\n'
        'import type { RouteRecordRaw } from "vue-router";\n'
        'const routes: RouteRecordRaw[] = [...];\n\n'
        '// Composables types\n'
        'interface Props { title: string; count?: number; }\n'
        'const props = withDefaults(defineProps<Props>(), { count: 0 });\n\n'
        '// API responses\n'
        'export interface XResponse { id: string; }\n'
        '```\n\n'
        '## Forbidden\n\n'
        '- Do not use any\n'
        '- Do not disable strict mode per-file\n'
        '- Do not use as cast to silence errors\n'
        '- Do not implement against this phantom package\n'
    )


def write_phantom(spec_name):
    spec_dir = ROOT / '.trellis' / 'spec' / spec_name / 'frontend'
    spec_dir.mkdir(parents=True, exist_ok=True)
    write_hook(spec_dir, spec_name)
    write_state(spec_dir, spec_name)
    write_quality(spec_dir, spec_name)
    write_type(spec_dir, spec_name)


def main():
    written = 0
    for spec_name in PHANTOMS:
        try:
            write_phantom(spec_name)
            written += 1
        except Exception as e:
            print(f'  failed {spec_name}: {e}')
    print(f'wrote 4 sub-files for {written} phantom specs')


if __name__ == '__main__':
    main()
