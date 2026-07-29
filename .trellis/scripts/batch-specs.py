#!/usr/bin/env python3
"""Batch-write 4 shared sub-files for a list of packages.

Writes 4 files (hook-guidelines, state-management, quality-guidelines, type-safety) into
.trellis/spec/<spec_dir_name>/frontend/. Use after directory-structure + component-guidelines are written.

Usage:
    python3 .trellis/scripts/batch-specs.py <kind> <spec_dir_name> <pkg_name>

Kinds: app-vue | mock | lib-config | lib-const | lib-i18n | lib-stores | lib-icons | lib-style | lib-helper
"""
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')


def mkdir_safe(d: Path) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_app_vue(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text(
        "# " + name + " Custom Hooks\n\n"
        "> Don't write new hooks unless absolutely necessary.\n\n"
        "## Built-ins (always check first)\n\n"
        "| Concern | Hook | Source |\n"
        "|---|---|---|\n"
        "| App config | usePreferences() | @vben/preferences |\n"
        "| Pinia stores | useAccessStore, useUserStore, useAuthStore | @vben/stores |\n"
        "| i18n | useI18n() | vue-i18n |\n"
        "| Router | useRouter(), useRoute() | vue-router |\n"
        "| Form | useVbenForm() | @vben/common-ui |\n"
        "| Table | useVbenVxeGrid() | @vben/plugins/vxe-table |\n\n"
        "## When to Write a New Hook\n\n"
        "- Used by >= 3 views / components\n"
        "- Returns reactive state OR stable async function\n"
        "- Non-trivial logic (> 10 lines)\n\n"
        "## Convention\n\n"
        "- use-<name>.ts (kebab-case, `use` prefix)\n"
        "- Co-located for one-feature hooks; shared under src/hooks/\n\n"
        "## Forbidden\n\n"
        "- Don't wrap usePreferences() in another useFoo()\n"
        "- Don't put pure business logic in a hook\n"
        "- Don't use hooks outside <script setup>\n"
    )

    (spec_dir / 'state-management.md').write_text(
        "# " + name + " State Management\n\n"
        "> Pick the simplest container that fits. Don't reach for Pinia first.\n\n"
        "## Decision Tree\n\n"
        "| Where the state lives | Use |\n"
        "|---|---|\n"
        "| One component, one render | ref() / reactive() |\n"
        "| One component, deep children | provide() / inject() |\n"
        "| Cross-page, persisted | preferences store |\n"
        "| Cross-page, transient | Pinia store (@vben/stores) |\n"
        "| Server cache | API + useAsyncResource |\n\n"
        "## Pinia Stores (canonical 3)\n\n"
        "- useAccessStore - tokens / access routes / flags\n"
        "- useAuthStore - login / logout / token expiry\n"
        "- useUserStore - current user, avatar, homePath\n\n"
        "## App-Specific Pattern\n\n"
        "`preferences.ts` may declare a typed preferences extension.\n"
    )

    (spec_dir / 'quality-guidelines.md').write_text(
        "# " + name + " Quality Guidelines\n\n"
        "> Strict-mode TS + 4-space + OxLint + ESLint + Stylelint + Commitlint.\n\n"
        "## Style\n\n"
        "- 4 spaces indent\n"
        "- Single quotes TS; double quotes HTML\n"
        "- No semicolons\n"
        "- Max line 120\n"
        "- Trailing newline\n\n"
        "## Naming\n\n"
        "| Thing | Convention |\n"
        "|---|---|\n"
        "| Page file | PascalCase.vue |\n"
        "| Component | kebab-case.vue |\n"
        "| Composable | useCamelCase |\n"
        "| Utility | kebab-case.ts |\n"
        "| Pinia store | useXxxStore |\n"
        "| Constant | UPPER_SNAKE_CASE |\n\n"
        "## Forbidden\n\n"
        "- Don't use any\n"
        "- Don't add @ts-ignore without comment\n"
        "- Don't bypass hooks with --no-verify\n"
        "- Don't commit .env or secrets\n"
    )

    (spec_dir / 'type-safety.md').write_text(
        "# " + name + " Type Safety\n\n"
        "> Strict-mode TS via @vben/tsconfig/web-app.json.\n\n"
        "## Required Patterns\n\n"
        "### Route records\n"
        "```ts\nimport type { RouteRecordRaw } from 'vue-router';\nconst routes: RouteRecordRaw[] = [...];\n```\n\n"
        "### API responses\n"
        "```ts\nimport { requestClient } from '#/api/request';\n"
        "export async function fetchFoo() {\n"
        "  return requestClient.get<FooResponse>('/foo');\n}\n```\n\n"
        "### Props\n"
        "```vue\n<script setup lang=\"ts\">\n"
        "interface Props { title: string; count?: number; }\n"
        "const props = withDefaults(defineProps<Props>(), { count: 0 });\n</script>\n```\n\n"
        "## Type Imports\n\n"
        "Always `import type`:\n"
        "```ts\nimport type { RouteRecordRaw } from 'vue-router';\n```\n\n"
        "## Forbidden\n\n"
        "- Don't use any\n"
        "- Don't disable strict mode per-file\n"
        "- Don't `as` cast to silence errors\n"
        "- Don't @ts-ignore without comment\n"
    )


def write_mock(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": No Hooks\n\n> Nitro server - no Vue hooks.\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": In-Memory State\n\n> Mock backend uses in-memory data only.\n\n## Forbidden\n\n- Don't add a database\n- Don't persist auth tokens\n- Don't use cookies for state\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Mock-only strict-mode server code.\n\n## Style\n\n- 4 spaces TS\n- Single quotes\n- Async/await for endpoint handlers\n\n## Forbidden\n\n- Don't use Express\n- Don't use Generators\n- Don't commit .env\n- Don't console.log to debug\n\n## Start\n\n```bash\npnpm dev:backend-mock\n```\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Strict-mode TS for Nitro handlers.\n\n```ts\nimport { defineEventHandler, readBody, createError } from 'h3';\nexport default defineEventHandler(async (event) => { return {}; });\n```\n")


def write_lib_config(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": Not Applicable\n\n> Configuration packages don't have Vue hooks.\n\nIf runtime behavior needed, put it in @vben/node-utils or app composables.\n\n## Forbidden\n\n- Don't add Vue hooks here\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Stateless by Design\n\n> Configs are static.\n\n## Forbidden\n\n- Don't add mutable state\n- Don't export singletons\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Config-only package.\n\n## Style\n\n- 2 spaces JSON/YAML\n- 4 spaces TS\n\n## Forbidden\n\n- Don't add runtime functions\n- Don't add tests (TS compiler checks)\n- Don't make configs mutable\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Strict-mode TS.\n\n```ts\nimport type { Linter } from 'eslint';\nexport const config: Linter.Config[] = [...];\n```\n\n## Forbidden\n\n- Don't disable strict mode\n- Don't use any\n")


def write_lib_const(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": No Hooks\n\n> Pure constants / types package. No Vue hooks.\n\nApps consume via composables in their own code:\n\n```ts\nimport { usePreferences } from '@vben/preferences';\nimport { LAYOUTS } from '" + name + "';\n```\n\n## Forbidden\n\n- Don't add Vue hooks here\n- Don't add reactive state\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Pure Data\n\n> Constants / types are static values, no runtime state.\n\n## Forbidden\n\n- Don't add module-level mutable variables\n- Don't add runtime-fetched values\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Strict-mode TS, zero runtime deps.\n\n## Style\n\n- 4 spaces TS\n- Single quotes\n- Trailing newline\n\n## Forbidden\n\n- Don't introduce dependencies\n- Don't add tests\n- Don't add async functions\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Strict-mode TS. Zero runtime concerns.\n\n```ts\nexport type AccessToken = null | string;\nexport const LAYOUTS = ['sidebar-nav', 'mixed-nav'] as const;\n```\n\n## Forbidden\n\n- Don't use any\n- Don't use Object as a type\n")


def write_lib_i18n(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": No Hooks\n\n> Pure data. useI18n() is from vue-i18n in apps.\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Static Data\n\n> Build-time static. No runtime state.\n\n## Forbidden\n\n- Don't add mutable state\n- Don't load async at runtime\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Static JSON.\n\n## Style\n\n- 2 spaces JSON\n- Camel-case keys\n- Double-quoted strings\n\n## Forbidden\n\n- Don't put non-translation data here\n- Don't use flat keys\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Locales typed via vue-i18n.\n\n```ts\ndeclare module 'vue-i18n' {\n  interface DefineLocaleMessage { auth: typeof enUS.auth; page: typeof enUS.page; }\n}\n```\n\n## Forbidden\n\n- Don't use any\n- Don't import raw JSON in app code\n")


def write_lib_stores(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": Store vs Hook\n\n> Pinia stores ARE the hook pattern.\n\n## Forbidden\n\n- Don't add Vue hooks inside defineStore\n- Don't duplicate store state in composables\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Cross-page State\n\n> Pinia is canonical shared transient state.\n\n## Persistence\n\nThis package is transient. Persisted -> @vben/preferences.\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Strict-mode TS, setup-style stores.\n\n## Style\n\n- 4 spaces TS, single quotes, no any\n\n## Naming\n\n| Thing | Convention |\n|---|---|\n| Store hook | useXxxStore |\n| State | camelCase |\n| Action | verb + noun |\n\n## Forbidden\n\n- Don't use Options API\n- Don't put APIs in store factories\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Strict-mode TS.\n\n```ts\nimport { ref } from 'vue';\nimport { defineStore } from 'pinia';\nexport const useAccessStore = defineStore('access', () => {\n  const x = ref(null);\n  return { x };\n});\n```\n")


def write_lib_icons(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": No Hooks\n\n> Icon components render-only.\n\nIf dynamic switching needed, wrap outside this package:\n\n```ts\nimport { usePreferences } from '@vben/preferences';\nimport { computed } from 'vue';\nexport function useThemeIcon() {\n  const p = usePreferences();\n  return computed(() => p.theme.mode === 'dark' ? 'lucide:moon' : 'lucide:sun');\n}\n```\n\n## Forbidden\n\n- Don't add Vue hooks here\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Stateless Icons\n\n> Icons are pure render components. No reactive state.\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> SVG + Iconify. Tree-shake critical.\n\n## Forbidden\n\n- Don't bundle full icon set\n- Don't inline <svg> in views\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Vue SFC + IconifyIcon props typed.\n\n```ts\nimport type { PropType } from 'vue';\nexport default defineComponent({\n  props: {\n    icon: { type: String as PropType<string>, required: true },\n    size: { type: Number, default: 16 },\n  },\n});\n```\n")


def write_lib_style(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": No Vue Hooks\n\n> Pure CSS package.\n\nApps consume styles via Tailwind utility classes.\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Per-Framework Static CSS\n\n> CSS is static. Theme state owned by apps (preferences).\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Per-framework CSS bundle.\n\n## Style\n\n- 2 spaces CSS, 4 spaces SCSS\n- Mobile-first responsive\n\n## Forbidden\n\n- Don't import other framework's components\n- Don't redefine Tailwind tokens\n- Don't add JS to .css files\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> CSS package. style-exports.d.ts for TS.\n\n```ts\ndeclare module '*.css' {\n  const content: string;\n  export default content;\n}\n```\n")


def write_lib_helpers(spec_dir: Path, name: str) -> None:
    mkdir_safe(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text("# " + name + ": No Vue Hooks\n\n> Helper lib has no Vue hooks.\n\nApps wrap helpers in composables if reactivity needed.\n\n## Forbidden\n\n- Don't add Vue-specific code\n- Don't add reactive state to this package\n")
    (spec_dir / 'state-management.md').write_text("# " + name + ": Stateless\n\n> Helper package is stateless. No caches, no globals.\n\n## Forbidden\n\n- Don't add module-level mutable state\n- Don't add singletons\n")
    (spec_dir / 'quality-guidelines.md').write_text("# " + name + " Quality Guidelines\n\n> Strict-mode TS, 4-space, single quotes.\n\n## Tests\n\nCo-located tests: __tests__/<name>.test.ts\n\n```bash\npnpm --filter " + name + " test\n```\n\n## Forbidden\n\n- Don't introduce dependencies\n- Don't add side-effect imports\n")
    (spec_dir / 'type-safety.md').write_text("# " + name + " Type Safety\n\n> Strict-mode TS.\n\n## Forbidden\n\n- Don't use any\n- Don't `as` cast to silence errors\n")


KIND_WRITERS = {
    'app-vue': write_app_vue,
    'mock': write_mock,
    'lib-config': write_lib_config,
    'lib-const': write_lib_const,
    'lib-i18n': write_lib_i18n,
    'lib-stores': write_lib_stores,
    'lib-icons': write_lib_icons,
    'lib-style': write_lib_style,
    'lib-helper': write_lib_helpers,
}


def main() -> None:
    if len(sys.argv) != 4:
        print('usage: batch-specs.py <kind> <spec_dir_name> <pkg_name>')
        print('kinds:', list(KIND_WRITERS.keys()))
        sys.exit(1)

    kind = sys.argv[1]
    spec_dir_name = sys.argv[2]
    name = sys.argv[3]

    if kind not in KIND_WRITERS:
        print('kind ' + str(kind) + ' not in ' + str(list(KIND_WRITERS.keys())))
        sys.exit(1)

    spec_dir = ROOT / '.trellis' / 'spec' / spec_dir_name / 'frontend'
    KIND_WRITERS[kind](spec_dir, name)
    print('wrote 4 files to ' + str(spec_dir) + ' (' + str(kind) + ')')


if __name__ == '__main__':
    main()
