# @vben/tsconfig

> vben monorepo package `@vben/tsconfig` (v5.7.0) — HolOS built with 本包 and customized config.

## 概述

Configuration package for **@vben/tsconfig** — provides shared TS / lint / style config used across the monorepo.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**: (no scripts)
- **Deps** (top): @vben/types, vite

> HolOS (`@vben/web-holos`) consumes 本包 via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## 目录结构

```
base.json
library.json
node.json
package.json
web-app.json
web.json
```

## 约定 for @vben/tsconfig

1. 通过 `src/index.ts` re-export —— 单一入口，不做内部深导入
2. 同级文件使用 `'.'` 相对路径导入 for sibling files; use workspace name for cross-package imports
3. 在...中添加新规则时必须升级版本 **@vben/tsconfig**
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
