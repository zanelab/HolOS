#!/usr/bin/env python3
"""Write 2 sub-files (directory-structure + component-guidelines) per package.

Usage:
    python3 .trellis/scripts/batch-2-specs.py <kind> <spec_dir_name> <pkg_name>
"""
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')


def mkdir_safe(d):
    d.mkdir(parents=True, exist_ok=True)
    return d


def t_app_vue(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Vue 3 + UI-framework conventions.\n\n'
        '## Tree (verified 2026-07-30)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # name "' + name + '" v5.7.0\n'
        '├── vite.config.ts              # uses @vben/vite-config\n'
        '├── tsconfig.json\n'
        '├── index.html\n'
        '├── public/\n'
        '└── src/\n'
        '    ├── main.ts                 # initPreferences + dynamic import("./bootstrap")\n'
        '    ├── bootstrap.ts\n'
        '    ├── app.vue\n'
        '    ├── preferences.ts          # defineOverridesPreferences\n'
        '    ├── adapter/                # UI-framework adapter (flavor-specific)\n'
        '    │   ├── form.ts\n'
        '    │   └── vxe-table.ts\n'
        '    ├── api/\n'
        '    │   ├── index.ts\n'
        '    │   ├── request.ts\n'
        '    │   └── core/{auth,user,menu}.ts\n'
        '    ├── layouts/{basic,auth}.vue\n'
        '    ├── locales/index.ts + langs/{zh-CN,en-US}\n'
        '    ├── router/{index.ts, guard.ts, access.ts, routes/{core,index,modules}}\n'
        '    ├── store/\n'
        '    └── views/\n'
        '        ├── _core/{about,profile,authentication,fallback}\n'
        '        ├── dashboard/{analytics,workspace}\n'
        '        └── demos/<flavor>/\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Adapter layer** isolates UI-framework code\n'
        '- **API surface** through src/api/request.ts\n'
        '- **Routes** core.ts framework-only, modules/<feature> business\n'
        '- **Locales** zh-CN and en-US both land in same commit\n\n'
        '## Forbidden\n\n'
        "- Don't import UI lib directly outside src/adapter\n"
        "- Don't add routes to routes/core.ts\n"
        "- Don't fetch() in views\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' Component Guidelines\n\n'
        '> Vue 3 + UI-framework conventions.\n\n'
        '## Conventions\n\n'
        '- **<script setup lang="ts">** only\n'
        '- **UI-framework** imported through adapters\n'
        '- **i18n** via $t("namespace.key")\n'
        '- **<VbenForm>** + **<VbenVxeGrid>** from @vben/common-ui + @vben/plugins/vxe-table\n\n'
        '## Example: analytics view\n\n'
        '```vue\n'
        '<script setup lang="ts">\n'
        'import { onMounted, ref } from "vue";\n'
        'import { fetchAnalytics } from "#/api";\n'
        'const data = ref<AnalyticsData[]>([]);\n'
        'onMounted(async () => { data.value = await fetchAnalytics(); });\n'
        '</script>\n'
        '<template>\n'
        '  <Page>\n'
        '    <Card :title="$t(\'page.dashboard.analytics\')">\n'
        '      <VChart :option="chartOption" />\n'
        '    </Card>\n'
        '  </Page>\n'
        '</template>\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't import UI lib directly from views\n"
        "- Don't mutate props in <script setup>\n"
        "- Don't use v-html (XSS)\n"
        "- Don't use defineComponent({...})\n"
    )


def t_mock(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Mock backend built on **Nitro**.\n\n'
        '## Tree (verified)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # name "' + name + '" v5.7.0\n'
        '├── nitro.config.ts\n'
        '├── tsconfig.json + tsconfig.build.json\n'
        '├── error.ts                    # h3 createError helper\n'
        '├── README.md\n'
        '└── src/\n'
        '    ├── api/                    # <resource>.<method>.ts handlers\n'
        '    │   ├── auth/    (login.post.ts, logout.post.ts)\n'
        '    │   ├── demo/\n'
        '    │   ├── menu/\n'
        '    │   ├── system/\n'
        '    │   ├── table/\n'
        '    │   ├── timezone/\n'
        '    │   └── user/\n'
        '    ├── middleware/\n'
        '    ├── routes/\n'
        '    └── utils/\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Mock endpoints** use same path as production (`/api/...`)\n'
        '- **Filename convention**: `<resource>.<method>.ts` (e.g. `login.post.ts`)\n'
        '- **Run via** `pnpm dev:backend-mock` (port 5320)\n\n'
        '## Forbidden\n\n'
        "- Don't use Express - use h3\n"
        "- Don't put real auth here - mock only\n"
        "- Don't add a real database\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' Component Guidelines\n\n'
        '> Nitro Mock Server "Components" = HTTP endpoints.\n\n'
        '## Pattern: defineEventHandler\n\n'
        '```ts\n'
        'import { defineEventHandler, readBody, createError } from "h3";\n'
        'export default defineEventHandler(async (event) => {\n'
        '  const body = await readBody(event);\n'
        '  if (!body.username) throw createError({ statusCode: 400 });\n'
        '  return { access_token: "mock-token" };\n'
        '});\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't use Express\n"
        "- Don't use Generators\n"
    )


def t_lib_config(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Config-only package consumed via workspace alias.\n\n'
        '## Tree (verified)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # workspace name "' + name + '"\n'
        '├── tsconfig.json\n'
        '└── src/\n'
        '    ├── index.ts                # re-exports everything\n'
        '    └── (one or more config files)\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Config objects** exported as named const\n'
        '- **Single barrel** at src/index.ts\n'
        '- **No real build step** - consumed via tsx\n'
        '- **scripts/stub.mjs** provides fake dist/index.mjs\n\n'
        '## Forbidden\n\n'
        "- Don't add runtime code (HTTP, file IO, async)\n"
        "- Don't add CLI\n"
        "- Don't add tests\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' "Component" Style - Config Object\n\n'
        '> No Vue components. "Components" are typed config objects.\n\n'
        '## Pattern\n\n'
        '```ts\n'
        'import type { Linter } from "eslint";\n'
        'export const config: Linter.Config[] = [\n'
        '  /* config entries */\n'
        '];\n'
        '```\n\n'
        '## Usage\n\n'
        '```ts\n'
        'import { config as eslintConfig } from "' + name + '";\n'
        'export default [\n'
        '  ...eslintConfig,\n'
        '  // app-specific overrides\n'
        '];\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't add side-effect functions\n"
        "- Don't add CLI/runtime code\n"
        "- Don't import runtime deps - zero-dep\n"
    )


def t_lib_const(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Pure constants/types/preferences utilities package.\n\n'
        '## Tree (verified)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # workspace name "' + name + '"\n'
        '├── tsconfig.json\n'
        '└── src/\n'
        '    ├── index.ts                # public barrel\n'
        '    └── (constants.ts | types.ts | config.ts)\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Single barrel** at index.ts\n'
        '- **Pure values/types only** - no IO\n'
        '- **Tree-shake friendly** - each export individually named\n\n'
        '## Forbidden\n\n'
        "- Don't add Vue code\n"
        "- Don't import runtime dependencies\n"
        "- Don't bundle into classes / namespaces\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' "Component" Style - Constants / Types\n\n'
        '## Pattern: explicit named exports\n\n'
        '```ts\n'
        "export const LOGIN_PATH = '/auth/login';\n"
        'export type LayoutType = "sidebar-nav" | "mixed-nav" | /* ... */\n'
        'export interface UserInfo {\n'
        '  id: string;\n'
        '  realName: string;\n'
        '}\n'
        '```\n\n'
        '## Usage\n\n'
        '```ts\n'
        "import { LOGIN_PATH, type UserInfo, type LayoutType } from '" + name + "';\n"
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't add IO functions\n"
        "- Don't add Vue refs\n"
        "- Don't bundle into namespaced objects\n"
    )


def t_lib_i18n(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> i18n locales package - vue-i18n source of truth.\n\n'
        '## Tree (verified)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # name "@vben/locales" v5.7.0\n'
        '├── tsconfig.json\n'
        '├── i18n.ts                     # $t wrapper\n'
        '├── typing.ts                   # locale types\n'
        '├── index.ts                    # setupI18n + loadMessages\n'
        '└── langs/\n'
        '    ├── zh-CN/\n'
        '    │   ├── auth.json\n'
        '    │   ├── common.json\n'
        '    │   ├── demos.json\n'
        '    │   └── page.json\n'
        '    └── en-US/...\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Top-level keys**: auth, common, demos, page - each maps to its own JSON\n'
        '- **Nested keys** allowed: page.home.title, demos.vben.title\n'
        '- **Both languages land in same commit**\n'
        '- **fallbackLocale** is en-US\n\n'
        '## Forbidden\n\n'
        "- Don't put i18n strings in Vue components\n"
        "- Don't put translation logic here\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' Component Guidelines\n\n'
        '> No Vue components. Source of truth = JSON locale files.\n\n'
        '## Pattern\n\n'
        '```json\n'
        '{\n'
        '  "auth": {\n'
        '    "login": "Login"\n'
        '  },\n'
        '  "page": {\n'
        '    "home": {\n'
        '      "title": "Home"\n'
        '    }\n'
        '  }\n'
        '}\n'
        '```\n\n'
        '## Usage\n\n'
        '```vue\n'
        '<script setup>\n'
        'import { useI18n } from "vue-i18n";\n'
        'const { t } = useI18n();\n'
        '</script>\n'
        '<template>\n'
        '  <h1>{{ t(\'page.home.title\') }}</h1>\n'
        '</template>\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't put strings in Vue components\n"
        "- Don't use Chinese / English strings directly\n"
    )


def t_lib_stores(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Pinia stores shared across all web-* apps.\n\n'
        '## Tree (verified from packages/stores/)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # name "@vben/stores" v5.7.0\n'
        '├── tsconfig.json\n'
        '├── setup.ts                    # createPinia + plugins\n'
        '├── index.ts                    # re-exports stores\n'
        '└── modules/\n'
        '    ├── access.ts               # useAccessStore\n'
        '    ├── auth.ts                 # useAuthStore\n'
        '    └── user.ts                 # useUserStore\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **One store per module file**\n'
        '- **Setup-style stores** (defineStore("id", () => ...))\n'
        '- **All stores registered in index.ts**\n\n'
        '## Forbidden\n\n'
        "- Don't put business logic in setup()\n"
        "- Don't put API calls inside setup()\n"
        "- Don't create circular deps between stores\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' "Component" Style - Pinia Stores\n\n'
        '> No Vue components. Stores = Pinia state + actions.\n\n'
        '## Pattern: setup-style store\n\n'
        '```ts\n'
        'import { defineStore } from "pinia";\n'
        'export const useAccessStore = defineStore("access", () => {\n'
        '  const accessToken = ref<AccessToken>(null);\n'
        '  function setAccessMenus(menus: RouteRecordStringComponent[]) {\n'
        '    accessMenus.value = menus;\n'
        '  }\n'
        '  return { accessToken, setAccessMenus };\n'
        '});\n'
        '```\n\n'
        '## Usage\n\n'
        '```vue\n'
        '<script setup>\n'
        'import { useAccessStore } from "' + name + '";\n'
        'const accessStore = useAccessStore();\n'
        'accessStore.setAccessMenus(menus);\n'
        '</script>\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't use Options API for stores\n"
        "- Don't define globals outside defineStore\n"
    )


def t_lib_icons(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Iconify + SVG icons. Used across all web-* apps.\n\n'
        '## Tree (verified)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # name "@vben/icons" v5.7.0\n'
        '├── index.ts                    # re-exports Svg*Icon + IconifyIcon\n'
        '└── svg/\n'
        '    ├── SvgAntdvLogoIcon.vue\n'
        '    ├── SvgAntdvNextLogoIcon.vue\n'
        '    └── (... per-component SVG icons)\n'
        '```\n\n'
        '## Conventions\n\n'
        "- **<IconifyIcon :icon=\"name\">** - runtime-loaded from Iconify API\n"
        "- **<SvgFooIcon>** - local SVG components\n"
        "- **Tree-shaking**: import specific icons\n"
        "- **Auto-import**: via unplugin-vue-components\n\n"
        '## Forbidden\n\n'
        "- Don't bundle the full Iconify icon set\n"
        "- Don't add inline <svg> in templates\n"
        "- Don't import icons from react-icons\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' Component Guidelines\n\n'
        '## Pattern: IconifyIcon wrapper\n\n'
        '```vue\n'
        '<script setup lang="ts">\n'
        "import { Icon } from '@iconify/vue';\n"
        "defineProps<{ icon: string; size?: number }>();\n"
        '</script>\n'
        '<template>\n'
        '  <Icon :icon="icon" :width="size ?? 16" :height="size ?? 16" />\n'
        '</template>\n'
        '```\n\n'
        'Usage:\n\n'
        '```vue\n'
        '<IconifyIcon icon="lucide:home" :size="20" />\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't import raw icons from Iconify / @iconify/vue directly\n"
        "- Don't add <svg> inline to views\n"
    )


def t_lib_style(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Per-framework CSS bundle + global styles.\n\n'
        '## Tree (verified from packages/styles/)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # name "@vben/styles" v5.7.0\n'
        '├── index.ts                    # re-exports all flavors\n'
        '├── style-exports.d.ts          # CSS module declarations\n'
        '└── <flavor>/                   # per-UI-framework styles\n'
        '    ├── antd/\n'
        '    ├── ele/\n'
        '    ├── naive/\n'
        '    ├── antdv-next/\n'
        '    └── global/\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Per-flavor subdirs** isolated by UI framework\n'
        '- **global/** for cross-flavor utilities\n'
        '- **style-exports.d.ts** - CSS module .d.ts\n\n'
        '## Forbidden\n\n'
        "- Don't import other framework's components\n"
        "- Don't redefine Tailwind tokens\n"
        "- Don't add JS to .css / .scss\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' Component Guidelines\n\n'
        '> Pure CSS package. Apps consume styles via Tailwind utility classes.\n\n'
        '## Pattern: app-level CSS with framework imports\n\n'
        '```css\n'
        '/* apps/web-antd/src/index.css */\n'
        "@import url('@vben/styles/index');\n"
        '/* plus app-specific overrides */\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't mix framework CSS in same file\n"
        "- Don't redefine Tailwind tokens\n"
    )


def t_lib_helpers(spec, name):
    mkdir_safe(spec)
    spec.joinpath('directory-structure.md').write_text(
        '# ' + name + ' Directory Structure\n\n'
        '> Pure utility package - no UI, no Vue, no runtime.\n\n'
        '## Tree (verified from packages/utils/)\n\n'
        '```\n' + name + '/\n'
        '├── package.json                # workspace name "' + name + '"\n'
        '├── tsconfig.json\n'
        '├── index.ts                    # public barrel\n'
        '└── helpers/                    # various helper modules\n'
        '```\n\n'
        '## Conventions\n\n'
        '- **Single barrel** at index.ts\n'
        '- **Pure functions** only - no IO\n'
        '- **Tests in __tests__/ alongside source**\n\n'
        '## Forbidden\n\n'
        "- Don't add Vue code\n"
        "- Don't add side effects\n"
    )

    spec.joinpath('component-guidelines.md').write_text(
        '# ' + name + ' Component Guidelines\n\n'
        '> No Vue components. Functions only.\n\n'
        '## Pattern: explicit named exports\n\n'
        '```ts\n'
        'export function mergeRouteModules(modules: RouteModule[]): RouteRecordRaw[] {\n'
        '  // implementation\n'
        '}\n'
        '```\n\n'
        '## Usage\n\n'
        '```ts\n'
        "import { mergeRouteModules } from '" + name + "';\n"
        'const routes = mergeRouteModules([dashboardModule, demosModule]);\n'
        '```\n\n'
        '## Forbidden\n\n'
        "- Don't bundle into classes / namespaces\n"
        "- Don't add side effects\n"
        "- Don't return generic any\n"
    )


KIND_WRITERS = {
    'app-vue': t_app_vue,
    'mock': t_mock,
    'lib-config': t_lib_config,
    'lib-const': t_lib_const,
    'lib-i18n': t_lib_i18n,
    'lib-stores': t_lib_stores,
    'lib-icons': t_lib_icons,
    'lib-style': t_lib_style,
    'lib-helper': t_lib_helpers,
}


def main():
    if len(sys.argv) != 4:
        print('usage: batch-2-specs.py <kind> <spec_dir_name> <pkg_name>')
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
    print('wrote 2 files to ' + str(spec_dir) + ' (' + str(kind) + ')')


if __name__ == '__main__':
    main()
