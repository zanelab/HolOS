# @vben/node-utils

> vben monorepo package `@vben/node-utils` (v5.7.0) — HolOS built with 本包 and customized config.

## 概述

Package **@vben/node-utils** (v5.7.0) — vben monorepo shared library.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**：占位
- **Deps** (top): @changesets/git, @manypkg/get-packages, chalk, consola, dayjs, execa, find-up, ora

> HolOS (`@vben/web-holos`) consumes 本包 via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## 目录结构

```
constants.ts
date.ts
formatter.ts
fs.ts
git.ts
hash.ts
index.ts
monorepo.ts
path.ts
spinner.ts
```

## 约定 for @vben/node-utils

1. 单一 `src/index.ts` 入口 —— 只 re-export 公开 API
2. 内部 helpers 放在 `helpers/` 或 `utils/` 子目录
3. Use TypeScript 严格模式; no `any` (use `unknown` + narrowing)
4. Consume via `@vben` workspace alias (not relative paths)

## 禁止 Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/node`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
