# @vben/locales

> vben monorepo package `@vben/locales` (v5.7.0) — HolOS built with 本包 and customized config.

## 概述

Package **@vben/locales** (v5.7.0) — vben monorepo shared library.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**: (no scripts)
- **Deps** (top): @intlify/core-base, @vben-core/composables, vue, vue-i18n

> HolOS (`@vben/web-holos`) consumes 本包 via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## 目录结构

```
langs/
  en-US/
  zh-CN/
i18n.ts
index.ts
typing.ts
```

## 约定 for @vben/locales

1. 单一 `src/index.ts` 入口 —— 只 re-export 公开 API
2. 内部 helpers 放在 `helpers/` 或 `utils/` 子目录
3. Use TypeScript 严格模式; no `any` (use `unknown` + narrowing)
4. Consume via `@vben` workspace alias (not relative paths)

## 禁止 Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/locales`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
