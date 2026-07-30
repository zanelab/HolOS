# web-antdv-next Directory Structure

> Real layout for `apps/{'ui_lib': 'ant-design-vue v4', 'name_zh': 'Web-AntDV-Next (Ant Design Vue 4)', 'color_theme': 'compact', 'adapters': ['ant-design-vue/v4', '@vben/form-antdv'], 'icon': 'lucide:hexagon', 'lang': 'vue + ant-design-vue'} app/`. Source verified 2026-07-30.

## 目录树 (verified)

```
web-antdv-next/
├── package.json                    # name "web-antdv-next" v5.7.0
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
    │   ├── (component/index.ts)    # ant-design-vue v4 wrapper
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
        └── demos/{ 'ant-design-vue v4' }/  # flavor-specific demos
```

## 实际 Verified

`apps/web-antdv-next/src/preferences.ts`:
```ts
export const overridesPreferences = defineOverridesPreferences({
  app: { name: import.meta.env.VITE_APP_TITLE },
});
```

`apps/web-antdv-next/src/router/routes/core.ts`:
```ts
const coreRoutes: RouteRecordRaw[] = [
  { meta: { icon: 'lucide:home' }, name: 'Root', path: '/', redirect: preferences.app.defaultHomePath },
  // Auth, FallbackNotFound...
];
```

## Conventions

- **Adapter layer** 隔离 UI 框架 (`ant-design-vue v4`) — view code 只 import adapters
- **API surface** through `requestClient` — no direct `fetch()` in views
- **Routes** core.ts framework-only, modules/<feature>.ts business
- **Locales** zh-CN + en-US both in same commit
- **Enums** shared → @vben/constants; local → src/enums/

## Adapter Layer (改 for ant-design-vue v4)

```ts
// src/adapter/component/index.ts (verified)
import { Button as NsButton } from 'ant-design-vue v4';

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

- ❌ 不要 import `ant-design-vue v4` directly from views — go through src/adapter
- ❌ 不要 add routes to `routes/core.ts` — use `modules/`
- ❌ 不要 `fetch()` in views — use `requestClient`
- ❌ 不要 bypass layout via inline `<router-view>` in `modules/`
- ❌ 不要 mutate props in `<script setup>` (Vue 3 reactivity is one-way)
- ❌ 不要 commit `node_modules/`, `dist/`, `.vite/`
