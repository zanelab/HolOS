# web-ele Directory Structure

> Real layout for `apps/{'ui_lib': 'element-plus', 'name_zh': 'Web-Ele (Element Plus)', 'color_theme': 'modern', 'adapters': ['element-plus', '@vben/form-ele'], 'icon': 'lucide:square', 'lang': 'vue + element-plus'} app/`. Source verified 2026-07-30.

## 目录树 (verified)

```
web-ele/
├── package.json                    # name "web-ele" v5.7.0
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
    │   ├── (component/index.ts)    # element-plus wrapper
    │   └── vxe-table.ts            # 表格 adapter
    ├── api/
    │   ├── index.ts
    │   ├── request.ts              # requestClient axios wrapper
    │   └── core/{auth, user, menu}.ts
    ├── layouts/
    │   ├── basic.vue               # BasicLayout (与 tdesign / antd 通用)
    │   ├── auth.vue                # AuthPageLayout
    │   └── index.ts
    ├── locales/
    │   ├── index.ts
    │   └── langs/{zh-CN, en-US}/...
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
        ├── _core/{about, profile, authentication, fallback}/
        ├── dashboard/{analytics, workspace}/
        └── demos/{ 'element-plus' }/  # flavor-specific demos
```

## 实际 Verified

`apps/web-ele/src/preferences.ts`:
```ts
export const overridesPreferences = defineOverridesPreferences({
  app: { name: import.meta.env.VITE_APP_TITLE },
});
```

`apps/web-ele/src/router/routes/core.ts`:
```ts
const coreRoutes: RouteRecordRaw[] = [
  { meta: { icon: 'lucide:home' }, name: 'Root', path: '/', redirect: preferences.app.defaultHomePath },
  // Auth, FallbackNotFound...
];
```

## Conventions

- **Adapter layer** 隔离 UI 框架 (`element-plus`) — view code 只 import adapters
- **API surface** through `requestClient` — no direct `fetch()` in views
- **Routes** core.ts framework-only, modules/<feature>.ts business
- **Locales** zh-CN + en-US both in same commit
- **Enums** shared → @vben/constants; local → src/enums/

## Adapter Layer (改 for element-plus)

```ts
// src/adapter/component/index.ts (verified)
import { Button as NsButton } from 'element-plus';

export const Button = {
  install(app, options) {
    app.use(NsButton, {
      theme: options.theme ?? 'light',
    });
  },
};

// Etc for Input, Select, Modal, ...
```

## Forbidden

- ❌ 不要 import `element-plus` directly from views — go through src/adapter
- ❌ 不要 add routes to `routes/core.ts` — use `modules/`
- ❌ 不要 `fetch()` in views — use `requestClient`
- ❌ 不要 bypass layout via inline `<router-view>` in `modules/`
- ❌ 不要 mutate props in `<script setup>` (Vue 3 reactivity is one-way)
- ❌ 不要 commit `node_modules/`, `dist/`, `.vite/`
