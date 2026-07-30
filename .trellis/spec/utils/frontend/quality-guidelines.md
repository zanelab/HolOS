# @vben/utils Quality Guidelines

> Pure functions, tree-shake friendly, no IO surprises.

## Purpose

`@vben/utils` is the workspace's pure-function package. The quality bar
is: every function is deterministic, every signature is typed, no
hidden state, no Vue runtime leak.

## TS file style

```ts
// packages/utils/src/helpers/find-menu-by-path.ts (real)
import type { MenuRecordRaw } from '@vben-core/typings';

function findMenuByPath(
  list: MenuRecordRaw[],
  path?: string,
): MenuRecordRaw | null {
  for (const menu of list) {
    if (menu.path === path) {
      return menu;
    }
    const findMenu = menu.children && findMenuByPath(menu.children, path);
    if (findMenu) {
      return findMenu;
    }
  }
  return null;
}

export { findMenuByPath, findRootMenuByPath };
```

- **2-space indent**
- **Single quotes**
- **No semicolons**
- **Trailing newline**
- **`import type`** for type-only imports
- **`export`** of named helpers only (no default)

## Real merge helper

```ts
// packages/utils/src/helpers/merge-route-modules.ts (verified)
interface RouteModuleType {
  default: RouteRecordRaw[];
}

function mergeRouteModules(
  routeModules: Record<string, unknown>,
): RouteRecordRaw[] {
  const mergedRoutes: RouteRecordRaw[] = [];
  for (const routeModule of Object.values(routeModules)) {
    const moduleRoutes = (routeModule as RouteModuleType)?.default ?? [];
    mergedRoutes.push(...moduleRoutes);
  }
  return mergedRoutes;
}

export { mergeRouteModules };
export type { RouteModuleType };
```

## Conventions

- **Pure functions** — no observable state between calls.
- **Return type annotation** — explicit, even when inferable.
- **No default exports** — named exports only.
- **No `console.log`** — debug in caller.
- **No `any`** in signatures — `unknown` if shape is unknown.
- **Tests in `__tests__/`** — unit only, no DOM tests for pure helpers.
- **`verbatimModuleSyntax`** — `import type` for type-only imports.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Helper file | `kebab-case.ts` | `find-menu-by-path.ts` |
| Function | `camelCase` verb-first | `findMenuByPath`, `generateMenus` |
| Type | `PascalCase` | `RouteModuleType` |
| Re-export | `export * from '...'` | `export * from './helpers';` |

## Linting & pre-commit

- ESLint flat config
- OxLint
- OxFmt
- Vitest (for helpers)
- `pnpm typecheck` includes `@vben/utils`

## Forbidden

- ❌ 不要 add `console.log` — debug in caller
- ❌ 不要 use `any` in signatures — `unknown` for opaque
- ❌ 不要 add `as` casts to silence type errors — refactor
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 add `default` exports — break tree-shaking
- ❌ 不要 depend on `@vben/stores` or `@vben/preferences` — pure functions
- ❌ 不要 add `getActivePinia()` here — wrong layer
- ❌ 不要 `Promise<void>` for sync helpers — sync only
