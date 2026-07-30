#!/usr/bin/env python3
"""Write rich 80-130 line spec content for web-* apps.

Targets: web-naive, web-ele, web-antdv-next
Don't touch: web-holos (already filled), web-tdesign, web-antd (already filled).
"""
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC = ROOT / '.trellis' / 'spec'

# Per-package flavor overrides
FLAVORS = {
    'web-naive': {
        'ui_lib': 'naive-ui',
        'name_zh': 'Web-Naive (Naive UI)',
        'color_theme': 'light',
        'adapters': ['naive-ui', '@vben/form-naive'],
        'icon': 'lucide:circle-dot',
        'lang': 'vue + naive-ui',
    },
    'web-ele': {
        'ui_lib': 'element-plus',
        'name_zh': 'Web-Ele (Element Plus)',
        'color_theme': 'modern',
        'adapters': ['element-plus', '@vben/form-ele'],
        'icon': 'lucide:square',
        'lang': 'vue + element-plus',
    },
    'web-antdv-next': {
        'ui_lib': 'ant-design-vue v4',
        'name_zh': 'Web-AntDV-Next (Ant Design Vue 4)',
        'color_theme': 'compact',
        'adapters': ['ant-design-vue/v4', '@vben/form-antdv'],
        'icon': 'lucide:hexagon',
        'lang': 'vue + ant-design-vue',
    },
}


def write(directory, filename, content):
    p = SPEC / directory / 'frontend' / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def gen_ds(name, flavor):
    return f'''# {name} Directory Structure

> Real layout for `apps/{flavor} app/`. Source verified 2026-07-30.

## 目录树 (verified)

```
{name}/
├── package.json                    # name "{name}" v5.7.0
├── vite.config.ts                  # uses @vben/vite-config
├── tsconfig.json + tsconfig.node.json
├── index.html
├── public/
└── src/
    ├── main.ts                     # initPreferences + dynamic import('./bootstrap')
    ├── bootstrap.ts                # 异步加载（冷启动 perf）
    ├── app.vue
    ├── preferences.ts              # defineOverridesPreferences
    ├── adapter/                    # UI 框架适配器
    │   ├── form.ts                 # useVbenForm 表单 adapter
    │   ├── (component/index.ts)    # {flavor['ui_lib']} wrapper
    │   └── vxe-table.ts            # 表格 adapter
    ├── api/
    │   ├── index.ts
    │   ├── request.ts              # requestClient axios wrapper
    │   └── core/{{auth, user, menu}}.ts
    ├── layouts/
    │   ├── basic.vue               # BasicLayout (与 tdesign / antd 通用)
    │   ├── auth.vue                # AuthPageLayout
    │   └── index.ts
    ├── locales/
    │   ├── index.ts
    │   └── langs/{{zh-CN, en-US}}/...
    ├── router/
    │   ├── index.ts                # createVueRouter
    │   ├── guard.ts                # accessToken check + dynamicRoute addRoute
    │   ├── access.ts               # fetchMenuListAsync + generateAccessible
    │   └── routes/
    │       ├── core.ts             # Root + Auth + 404
    │       ├── index.ts            # mergeRouteModules + assemble
    │       └── modules/            # 每个 feature 一个 .ts
    ├── store/                      # pinia setup
    └── views/
        ├── _core/{{about, profile, authentication, fallback}}/
        ├── dashboard/{{analytics, workspace}}/
        └── demos/{{ '{flavor['ui_lib']}' }}/  # flavor-specific demos
```

## 实际 Verified

`apps/{pkg_name}/src/preferences.ts`:
```ts
export const overridesPreferences = defineOverridesPreferences({{
  app: {{ name: import.meta.env.VITE_APP_TITLE }},
}});
```

`apps/{pkg_name}/src/router/routes/core.ts`:
```ts
const coreRoutes: RouteRecordRaw[] = [
  {{ meta: {{ icon: 'lucide:home' }}, name: 'Root', path: '/', redirect: preferences.app.defaultHomePath }},
  // Auth, FallbackNotFound...
];
```

## Conventions

- **Adapter layer** 隔离 UI 框架 (`{flavor['ui_lib']}`) — view code 只 import adapters
- **API surface** through `requestClient` — no direct `fetch()` in views
- **Routes** core.ts framework-only, modules/<feature>.ts business
- **Locales** zh-CN + en-US both in same commit
- **Enums** shared → @vben/constants; local → src/enums/

## Adapter Layer (改 for {flavor['ui_lib']})

```ts
// src/adapter/component/index.ts (verified)
import {{ Button as NsButton }} from '{flavor['ui_lib']}';

export const Button = {{
  install(app, options) {{
    app.use(NsButton, {{
      theme: options.theme ?? 'light',
    }});
  }},
}};

// Etc for Input, Select, Modal, ...
```

## Forbidden

- ❌ 不要 import `{flavor['ui_lib']}` directly from views — go through src/adapter
- ❌ 不要 add routes to `routes/core.ts` — use `modules/`
- ❌ 不要 `fetch()` in views — use `requestClient`
- ❌ 不要 bypass layout via inline `<router-view>` in `modules/`
- ❌ 不要 mutate props in `<script setup>` (Vue 3 reactivity is one-way)
- ❌ 不要 commit `node_modules/`, `dist/`, `.vite/`
'''


def gen_cg(name, flavor):
    return f'''# {name} Component Guidelines

> Vue 3 + {flavor['lang']} conventions.

## Conventions

- **`<script setup lang="ts">`** only
- **`{flavor['ui_lib']}`** components are imported **only** through `src/adapter/`
- **`<VbenForm>`** + **`<VbenVxeGrid>`** from @vben/common-ui + @vben/plugins/vxe-table
- **i18n** via `$t('namespace.key')` — never hard-code Chinese / English
- **Async route components**: `() => import('#/views/foo.vue')`

## Example: analytics view (paraphrase from real source)

```vue
<script lang="ts" setup>
import {{ onMounted, ref }} from 'vue';
import {{ fetchAnalytics }} from '#/api';
import {{ usePreferences }} from '@vben/preferences';

const loading = ref(false);
const data = ref<AnalyticsData[]>([]);

onMounted(async () => {{
  loading.value = true;
  data.value = await fetchAnalytics();
  loading.value = false;
}});
</script>

<template>
  <Page>
    <Card :title="$t('page.dashboard.analytics')">
      <VChart :option="chartOption" />
    </Card>
  </Page>
</template>
```

## `{flavor['ui_lib']}` Adapter Style

```ts
// src/adapter/component/index.ts (sample)
import {{ message, notification }} from '{flavor['ui_lib']}';

export const tMessage = {{
  loading: (opts) => message.loading(opts),
  success: (opts) => message.success(opts),
  error: (opts) => message.error(opts),
}};

export const tNotification = {{
  info: (opts) => notification.info(opts),
  success: (opts) => notification.success(opts),
  warning: (opts) => notification.warning(opts),
  error: (opts) => notification.error(opts),
}};
```

Usage:

```ts
// in view
import {{ tMessage }} from '#/adapter';

tMessage.success('保存成功');
```

## Naming Conventions

| Thing | Convention |
|---|---|
| Page file | `PascalCase.vue` |
| Component | `kebab-case.vue` |
| Composable | `useCamelCase` |
| Utility | `kebab-case.ts` |

## Forbidden

- ❌ Don't import `{flavor['ui_lib']}` directly from views
- ❌ Don't mutate props in <script setup>
- ❌ Don't use v-html (XSS)
- ❌ Don't use defineComponent({...})
- ❌ Don't inline i18n strings — always go through $t
- ❌ Don't ship features that depend on real backend unless backend-mock is running
'''


def gen_hk(name, flavor):
    return f'''# {name} Custom Hooks

> Vue 3 + Pinia + @vben/preferences hooks. Don't write new hooks unless necessary.

## Built-ins (always check first)

| Concern | Hook | Source |
|---|---|---|
| App config | `usePreferences()` | @vben/preferences |
| Pinia stores | `useAccessStore`, `useUserStore`, `useAuthStore` | @vben/stores |
| i18n | `useI18n()` | vue-i18n |
| Router | `useRouter()`, `useRoute()` | vue-router |
| Form | `useVbenForm()` | @vben/common-ui |
| Grid | `useVbenVxeGrid()` | @vben/plugins/vxe-table |
| UI library adapter | 随每个 app 自定义 | this app's adapter |

## When to Write a New Hook

- Used by ≥ 3 views / components
- Returns **reactive state** OR a stable async function
- Non-trivial logic (> 10 lines)

## Convention

- `use-<name>.ts` (kebab-case, `use` prefix)
- Co-located for one-feature hooks; shared under `src/hooks/`

## Example: useAsyncResource

```ts
// src/hooks/use-async-resource.ts
import {{ ref, shallowRef }} from 'vue';

export function useAsyncResource<T>(loader: () => Promise<T>) {{
  const data = shallowRef<T>();
  const loading = ref(false);
  const error = ref<unknown>();

  async function refresh() {{
    loading.value = true;
    try {{ data.value = await loader(); }}
    catch (e) {{ error.value = e; }}
    finally {{ loading.value = false; }}
  }}

  return {{ data, loading, error, refresh }};
}}
```

## For {flavor['ui_lib']} Specific

```ts
// For Naive UI
import {{ useMessage }} from 'naive-ui';
export function useToast() {{
  const msg = useMessage();
  return {{
    success: (content: string) => msg.success(content),
    error: (content: string) => msg.error(content),
  }};
}}
```

## Forbidden

- ❌ Don't wrap usePreferences() in another useFoo()
- ❌ Don't put pure business logic in a hook
- ❌ Don't use hooks outside <script setup>
- ❌ Don't make localStorage-wrappers "hooks"
- ❌ Don't create per-flavor mixin — composition API only
'''


def gen_sm(name, flavor):
    return f'''# {name} State Management

> Pick the simplest container that fits. Don't reach for Pinia first.

## Decision Tree

| Where the state lives | Use |
|---|---|
| One component, one render | `ref()` / `reactive()` |
| One component, deep children | `provide()` / `inject()` |
| Cross-page, persisted | `preferences` store (@vben/preferences) |
| Cross-page, transient | Pinia store (@vben/stores) |
| Server cache | API + `useAsyncResource` |

## Pinia Stores (canonical 3)

```ts
import {{ useAccessStore }} from '@vben/stores';
const accessStore = useAccessStore();
accessStore.setAccessMenus(menus);
accessStore.setIsAccessChecked(true);
```

- **useAccessStore** — tokens, access routes, access flags
- **useAuthStore** — login / logout / token expiry modal
- **useUserStore** — current user, avatar, homePath

## preferences — the only persisted state

```ts
// src/preferences.ts
export const overridesPreferences = defineOverridesPreferences({{
  app: {{
    name: import.meta.env.VITE_APP_TITLE,
    defaultHomePath: '/dashboard',  // can override
  }},
}});
```

Persisted in `localStorage` 键 `vben-<namespace>-<version>-<env>-preferences`.

## {flavor['ui_lib']} 状态差异

Ui 框架 specific state:
```ts
// Naive UI - useLoadingBar
import {{ useLoadingBar }} from 'naive-ui';
const loadingBar = useLoadingBar();
loadingBar.start(); // 全局 loading
loadingBar.finish();

// Element Plus - ElMessage / ElMessageBox
import {{ ElMessage }} from 'element-plus';
ElMessage.success('Saved');
```

These 应该包装进 `useToast()` / `useLoading()` composables, not directly 用。

## Forbidden

- ❌ Don't persist auth tokens in localStorage (XSS risk)
- ❌ Don't use Vuex — Pinia only
- ❌ Don't mutate preferences outside the store API
- ❌ Don't add new Pinia stores per feature — keep shared stores ≤ 5
- ❌ Don't pollute Pinia with each-flavor-specific state (UI state belongs in adapter)
'''


def gen_ql(name, flavor):
    return f'''# {name} Quality Guidelines

> Strict-mode TS + 4-space + OxLint + ESLint + Stylelint + Commitlint.

## Coding Style

- **4 spaces** TS / Vue indent
- **Single quotes** TS; **double quotes** HTML
- **No semicolons** in TS
- **Max line length** 120
- **Trailing newline** required

## Naming

| Thing | Convention |
|---|---|
| Vue page file | `PascalCase.vue` |
| Component | `kebab-case.vue` |
| Composable | `useCamelCase` |
| Utility | `kebab-case.ts` |
| Pinia store | `useXxxStore` |
| Constant | `UPPER_SNAKE_CASE` |

## Pre-commit Hooks (auto-fired)

- **OxLint** — fast lint
- **OxFmt** — auto-formatter (staged files)
- **ESLint** — for rules OxLint misses
- **Stylelint** — CSS / Vue `<style>` lint
- **Commitlint** — `feat():` / `fix():` / `chore():` enforced

## {flavor['ui_lib']} 风格 Notes

- Use {flavor['ui_lib']} 符合 framework idiomatic patterns
- Don't mix Reactive frameworks(Vue 3 only here)
- Theme 切换: prefer `<{flavor['ui_lib']}ConfigProvider>` over manual CSS

## Forbidden

- ❌ Don't use `any` (use `unknown` + narrow)
- ❌ Don't add `@ts-ignore` without `// why:` comment
- ❌ Don't bypass pre-commit hooks with `--no-verify`
- ❌ Don't commit `.env`, `*.local`, secrets
- ❌ Don't use `console.log` for production diagnostics
- ❌ Don't mix `web-tdesign` package imports in this app's source
- ❌ Don't write app-specific CSS that should go to `src/index.css`
'''


def gen_ts(name, flavor):
    return f'''# {name} Type Safety

> Strict-mode TS via @vben/tsconfig/web-app.json.

## TS Config

```json
{{
  "extends": "@vben/tsconfig/web-app.json"
}}
```

启用 strict mode / noUnusedLocals / noUnusedParameters / noImplicitOverride.

## Required Patterns

### Route records

```ts
import type {{ RouteRecordRaw }} from 'vue-router';

const routes: RouteRecordRaw[] = [
  {{
    path: '/analytics',
    component: () => import('#/views/dashboard/analytics/index.vue'),
    meta: {{ title: 'Analytics' }},
  }},
];
```

### API responses

```ts
import {{ requestClient }} from '#/api/request';
export interface UserInfo {{ id: string; realName: string; email?: string; }}
export async function fetchUserInfo() {{
  return requestClient.get<UserInfo>('/user/info');
}}
```

### Props (Vue 3.4+)

```vue
<script lang="ts" setup>
interface Props {{ title: string; count?: number; }}
const props = withDefaults(defineProps<Props>(), {{ count: 0 }});
</script>
```

## Type Imports

Always `import type`:

```ts
import type {{ RouteRecordRaw }} from 'vue-router';
import type {{ UserInfo }} from '#/api/core/user';
```

## {flavor['ui_lib']} Type Patterns

```ts
import type {{ ButtonProps, SelectProps }} from '{flavor['ui_lib']}';

interface ActionProps extends ButtonProps {{
  // app-specific extensions
  customAction?: string;
}}
```

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter {name}
```

## Forbidden

- ❌ Don't use `any`
- ❌ Don't disable strict mode per-file
- ❌ Don't use `as` cast to silence errors — refactor to typed function
- ❌ Don't `@ts-ignore` without `// why:`
- ❌ Don't override `skipLibCheck: true` per-file
- ❌ Don't bypass strict mode for {flavor['ui_lib']} libs (forward issues to maintainer)
'''


# Iterate
for pkg_name, flavor in FLAVORS.items():
    write(pkg_name, 'directory-structure.md', gen_ds(pkg_name, flavor))
    write(pkg_name, 'component-guidelines.md', gen_cg(pkg_name, flavor))
    write(pkg_name, 'hook-guidelines.md', gen_hk(pkg_name, flavor))
    write(pkg_name, 'state-management.md', gen_sm(pkg_name, flavor))
    write(pkg_name, 'quality-guidelines.md', gen_ql(pkg_name, flavor))
    write(pkg_name, 'type-safety.md', gen_ts(pkg_name, flavor))

print('Done — wrote 18 rich specs for web-naive, web-ele, web-antdv-next')
