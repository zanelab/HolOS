# @vben/tailwind-config

> vben monorepo package `@vben/tailwind-config` (v5.7.0) — HolOS built with 本包 and customized config.

## 概述

Configuration package for **@vben/tailwind-config** — provides shared TS / lint / style config used across the monorepo.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**: (no scripts)
- **Deps** (top): @iconify/tailwind4, @tailwindcss/typography, tailwindcss, tw-animate-css

> HolOS (`@vben/web-holos`) consumes 本包 via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## 目录结构

```
index.ts
theme.css
```

## 约定 for @vben/tailwind-config

1. 通过 `src/index.ts` re-export —— 单一入口，不做内部深导入
2. 同级文件使用 `'.'` 相对路径导入 for sibling files; use workspace name for cross-package imports
3. 在...中添加新规则时必须升级版本 **@vben/tailwind-config**
4. 至少在 1 个应用中测试 (`@vben/web-antd` or web-holos) before merging

## 禁止 Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/vite-config`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
