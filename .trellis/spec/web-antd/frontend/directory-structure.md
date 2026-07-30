# @vben/web-antd Directory Structure

> 真实布局 for `apps/web-antd/` (Ant Design Vue flavor).

## 目录树 (verified 2026-07-29)

```
apps/web-antd/
├── package.json                # name "@vben/web-antd" v5.7.0
├── vite.config.ts              # uses @vben/vite-config
├── tsconfig.json
├── index.html
├── public/
└── src/
    ├── main.ts                 # initPreferences + dynamic import('./bootstrap')
    ├── bootstrap.ts            # async-loaded for cold-start perf
    ├── app.vue
    ├── preferences.ts          # defineOverridesPreferences + **definePreferencesExtension** (app-specific config!)
    ├── adapter/
    │   ├── component/         # flavor-specific component adapters
    │   ├── form.ts
    │   ├── antdv.ts
    │   └── vxe-table.ts
    ├── api/
    │   ├── index.ts
    │   ├── request.ts
    │   └── core/
    │       ├── index.ts
    │       ├── auth.ts         # /api/auth/*
    │       ├── user.ts         # /api/user/info
    │       └── menu.ts         # /api/menu/all
    ├── layouts/
    │   ├── index.ts
    │   ├── basic.vue
    │   └── auth.vue
    ├── locales/
    │   ├── index.ts
    │   └── langs/{zh-CN,en-US}/...
    ├── router/
    │   ├── index.ts
    │   ├── guard.ts            # accessToken check
    │   ├── access.ts           # fetchMenuListAsync + generateAccessible
    │   └── routes/{core.ts,index.ts,modules/}
    ├── store/
    │   ├── auth.ts             # auth store (not Pinia) — for app state
    │   └── index.ts
    └── views/
        ├── _core/{about,authentication,profile,fallback}/
        ├── dashboard/{analytics,workspace}/
        └── demos/antd/
```

## App-Specific Pattern

`preferences.ts` defines a **typed preferences extension**:

```ts
interface WebAntdPreferencesExtension {
  defaultTableSize: number;
  enableFormFullscreen: boolean;
  reportTitle: string;
  tenantMode: 'multi' | 'single';
}
```

This adds app-level settings tab in the preferences drawer.

## 约定

- See `/opt/data/workspace/holos/.trellis/spec/web-tdesign/frontend/directory-structure.md` for full conventions (identical structure)

## 禁止

- Don't add a new route to `routes/core.ts` — use `routes/modules/`
- Don't add i18n strings outside the `zh-CN` / `en-US` JSON files
