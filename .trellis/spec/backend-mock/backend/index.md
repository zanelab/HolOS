# @vben/backend-mock

> vben monorepo package `@vben/backend-mock` (v5.7.0) — HolOS built with 本包 and customized config.

## 概述

Package **@vben/backend-mock** (v5.7.0) — vben monorepo shared library.

- **版本**：5.7.0
- **类型**：module
- **Scripts**：build、start
- **Deps** (top): @faker-js/faker, jsonwebtoken, nitropack

> HolOS (`@vben/web-holos`) consumes 本包 via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## 目录结构

```
api/
  auth/
  demo/
  menu/
  system/
  table/
  timezone/
  user/
middleware/
routes/
utils/
error.ts
nitro.config.ts
package.json
README.md
tsconfig.build.json
tsconfig.json
```

## 约定 for @vben/backend-mock

1. 单一 `src/index.ts` 入口 —— 只 re-export 公开 API
2. 内部 helpers 放在 `helpers/` 或 `utils/` 子目录
3. Use TypeScript 严格模式; no `any` (use `unknown` + narrowing)
4. Consume via `@vben` workspace alias (not relative paths)

## 禁止模式

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/backend`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
