# @vben/node-utils

> vben monorepo package `@vben/node-utils` (v5.7.0) — HolOS built with this package and customized config.

## Overview

Package **@vben/node-utils** (v5.7.0) — vben monorepo shared library.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**: stub
- **Deps** (top): @changesets/git, @manypkg/get-packages, chalk, consola, dayjs, execa, find-up, ora

> HolOS (`@vben/web-holos`) consumes this package via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## Directory Structure

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

## Conventions for @vben/node-utils

1. Single `src/index.ts` entry — re-export public API only
2. Internal helpers stay in `helpers/` or `utils/` subdirs
3. Use TypeScript strict mode; no `any` (use `unknown` + narrowing)
4. Consume via `@vben` workspace alias (not relative paths)

## Forbidden Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/node`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
