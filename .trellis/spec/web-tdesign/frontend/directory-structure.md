# @vben/web-tdesign Directory Structure

> 真实布局 for `apps/web-tdesign/` (TDesign Vue Next flavor).

## 目录树 (verified 2026-07-29)

```
apps/web-tdesign/
├── package.json                # name "@vben/web-tdesign" v5.7.0
├── vite.config.ts              # uses @vben/vite-config
├── tsconfig.json
├── index.html
├── public/                     # static assets
└── src/
    ├── main.ts                 # bootstrap entry: initPreferences + dynamic import('./bootstrap')
    ├── bootstrap.ts            # async-loaded (perf, defers big deps)
    ├── app.vue                 # root <App><RouterView /> etc
    ├── preferences.ts          # defineOverridesPreferences (only app.name override by default)
    │
    ├── adapter/
    │   ├── component/index.ts  # TDesign Vue component adapters
    │   ├── form.ts             # useVbenForm adapter
    │   ├── tdesign.ts          # tdesign-vue-next message adapter
    │   └── vxe-table.ts        # vxe-table grid adapter
    │
    ├── api/
    │   ├── index.ts
    │   ├── request.ts          # axios wrapper, base url from VITE_GLOB_API_URL
    │   └── core/
    │       ├── index.ts
    │       ├── auth.ts         # /api/auth/login, /api/auth/logout, ...
    │       ├── user.ts         # /api/user/info
    │       └── menu.ts         # /api/menu/all — used in router/access.ts
    │
    ├── layouts/
    │   ├── index.ts            # re-exports BasicLayout, AuthPageLayout, IFrameView
    │   ├── basic.vue           # primary layout (header + sider + content)
    │   └── auth.vue            # auth pages layout
    │
    ├── locales/
    │   ├── index.ts            # i18n setup
    │   └── langs/
    │       ├── zh-CN/
    │       │   ├── auth.json, page.json, demos.json, common.json, ...
    │       └── en-US/
    │
    ├── router/
    │   ├── index.ts            # createVueRouter + guard
    │   ├── guard.ts            # accessToken check + dynamic routes addRoute
    │   ├── access.ts           # fetchMenuListAsync + generateAccess
    │   └── routes/
    │       ├── core.ts         # Root + Auth + 404
    │       ├── index.ts        # mergeRouteModules(dynamicGlob) + assemble routes
    │       └── modules/        # one file per feature, auto-globbed
    │           ├── dashboard.ts
    │           ├── demos.ts
    │           └── vben.ts
    │
    ├── store/                  # pinia setup
    ├── views/
    │   ├── _core/
    │   │   ├── about/index.vue
    │   │   ├── authentication/login.vue
    │   │   ├── profile/index.vue
    │   │   └── fallback/{not-found,forbidden}.vue
    │   ├── dashboard/{analytics,workspace}/index.vue
    │   └── demos/tdesign/index.vue
    │
    └── enums/                  # app-specific enums (or shared with @vben/constants)
```

## 约定

- **Adapter layer**: every UI framework-specific code (tdesign / antd / element / naive) lives in `src/adapter/`. The rest of the codebase should not import `tdesign-vue-next` directly.
- **API surface**: every HTTP call goes through `api/request.ts`'s `requestClient`. Don't `fetch` directly in views.
- **Routes**: business routes go in `routes/modules/<feature>.ts`. `core.ts` is for framework-mandatory routes only (Root / Auth / 404). Auto-discovered via `import.meta.glob`.
- **Locales**: `zh-CN` first, `en-US` second. New keys MUST go into BOTH files in the same commit.
- **Enums**: shared enums → `packages/constants`; local enums → `src/enums/`.

## 禁止

- ❌ Don't `import { xxx } from 'tdesign-vue-next'` directly outside `src/adapter/`.
- ❌ Don't add a new route to `core.ts` — put it in `routes/modules/<your-feature>.ts`.
- ❌ Don't `fetch(...)` in views — use `requestClient`.
- ❌ Don't bypass the layout via `<router-view>` inside `routes/modules/` — children inherit `BasicLayout` from Root automatically.
