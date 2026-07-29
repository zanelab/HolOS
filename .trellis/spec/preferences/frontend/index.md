# @vben/preferences

> vben monorepo package `@vben/preferences` (v5.7.0) — HolOS built with this package and customized config.

## Overview

Package **@vben/preferences** (v5.7.0) — vben monorepo shared library.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**: (no scripts)
- **Deps** (top): @vben-core/preferences, @vben-core/typings

> HolOS (`@vben/web-holos`) consumes this package via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## Directory Structure

```
index.ts
```

## Conventions for @vben/preferences

1. Single `src/index.ts` entry — re-export public API only
2. Internal helpers stay in `helpers/` or `utils/` subdirs
3. Use TypeScript strict mode; no `any` (use `unknown` + narrowing)
4. Consume via `@vben` workspace alias (not relative paths)

## Forbidden Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/preferences`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
