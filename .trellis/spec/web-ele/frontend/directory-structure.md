# @vben/web-ele Directory Structure

> Vue 3 +  UI-framework conventions.

## 目录树（2026-07-30 核对）

```
@vben/web-ele/
├── package.json                # name "@vben/web-ele" v5.7.0
├── vite.config.ts              # uses @vben/vite-config
├── tsconfig.json
├── index.html
├── public/
└── src/
    ├── main.ts                 # initPreferences + dynamic import("./bootstrap")
    ├── bootstrap.ts
    ├── app.vue
    ├── preferences.ts          # defineOverridesPreferences
    ├── adapter/                # UI-framework adapter (flavor-specific)
    │   ├── form.ts
    │   └── vxe-table.ts
    ├── api/
    │   ├── index.ts
    │   ├── request.ts
    │   └── core/{auth,user,menu}.ts
    ├── layouts/{basic,auth}.vue
    ├── locales/index.ts + langs/{zh-CN,en-US}
    ├── router/{index.ts, guard.ts, access.ts, routes/{core,index,modules}}
    ├── store/
    └── views/
        ├── _core/{about,profile,authentication,fallback}
        ├── dashboard/{analytics,workspace}
        └── demos/<flavor>/
```

## 约定

- **Adapter layer** isolates UI-framework code
- **API surface** through src/api/request.ts
- **Routes** core.ts framework-only, modules/<feature> business
- **Locales** zh-CN and en-US both land in same commit

## 禁止

- Don't import UI lib directly outside src/adapter
- Don't add routes to routes/core.ts
- 不要在视图层调用 fetch()
