# @vben/tsconfig

> vben monorepo package `@vben/tsconfig` (v5.7.0) — HolOS built with this package and customized config.

## Overview

Configuration package for **@vben/tsconfig** — provides shared TS / lint / style config used across the monorepo.

- **Version**: 5.7.0
- **Type**: module
- **Scripts**: (no scripts)
- **Deps** (top): @vben/types, vite

> HolOS (`@vben/web-holos`) consumes this package via pnpm workspace. The repo is initialized with **trellis init -u zane --claude**; see `.trellis/spec/` and `.trellis/tasks/` for project conventions.

## Directory Structure

```
base.json
library.json
node.json
package.json
web-app.json
web.json
```

## Conventions for @vben/tsconfig

1. Re-export via `src/index.ts` — single entry, no internal deep imports
2. Use `'.'` relative imports for sibling files; use workspace name for cross-package imports
3. Version bump is mandatory when adding new rules to **@vben/tsconfig**
4. Test on at least 1 app (`@vben/web-antd` or web-holos) before merging

## Forbidden Patterns

- ❌ Don't deep-import from package subdirs (`@vben/foo/internals/util`) — use public `index.ts` only
- ❌ Don't bypass `src/index.ts` with direct file imports — that defeats tree-shaking
- ❌ Don't introduce new build configurations in this directory — extend the base config from `@vben/vite-config`
- ❌ Don't commit `dist/`, `node_modules/`, or platform lockfiles — already in `.gitignore`

## Related

- See `.trellis/spec/lint-configs/` for shared lint conventions
- See `.trellis/spec/frontend-guidelines/index.md` for cross-package frontend patterns
- See `.trellis/workflow.md` for the development workflow
