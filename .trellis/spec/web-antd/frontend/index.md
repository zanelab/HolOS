# @vben/web-antd

> vben monorepo package `@vben/web-antd` (v5.7.0) — HolOS built with 本包 and customized config.

## 概述

Application package **@vben/web-antd** — a vite-based frontend app for the vben monorepo.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**：build、build:analyze、dev、preview、typecheck
- **Deps** (top): @vben/access, @vben/common-ui, @vben/constants, @vben/hooks, @vben/icons, @vben/layouts, @vben/locales, @vben/plugins

> HolOS (`@vben/web-holos`) consumes 本包 via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## 目录结构

```
adapter/
  component/
api/
  core/
layouts/
locales/
  langs/
    en-US/
    zh-CN/
router/
  routes/
    modules/
store/
views/
  _core/
    about/
    authentication/
    fallback/
    profile/
  dashboard/
    analytics/
    workspace/
  demos/
    antd/
app.vue
```

## 约定 for @vben/web-antd

1. Vite + Vue 3 +  TS, port 5666-ish (configured in `vite.config.ts`)
2. Use `defineOverridesPreferences` from `src/preferences.ts` to override defaults
3. i18n keys 放在 `src/locales/langs/<locale>/*.json` — nested under `page.*`, `demos.*`, `auth.*`, etc.
4. 路由： `core.ts`（BasicLayout / Auth / 404） + `modules/<name>.ts` (per-feature, auto-globbed)
5. 自定义布局覆盖 `apps/<app-name>/src/layouts/`

## 禁止 Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/web`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
