# @vben/utils Type Safety

> Strict signatures. Imports of `@vben-core/typings` types.

## Purpose

`@vben/utils` has the strictest type contracts in the workspace. Every
helper's argument list and return type is explicit, and silent `any` is
forbidden.

## Real signatures

```ts
// packages/utils/src/helpers/find-menu-by-path.ts
import type { MenuRecordRaw } from '@vben-core/typings';

function findMenuByPath(
  list: MenuRecordRaw[],
  path?: string,
): MenuRecordRaw | null;

function findRootMenuByPath(
  menus: MenuRecordRaw[],
  path?: string,
  level?: number,
): {
  findMenu: MenuRecordRaw | null;
  rootMenu: MenuRecordRaw | undefined;
  rootMenuPath: string | undefined;
};

export { findMenuByPath, findRootMenuByPath };
```

```ts
// packages/utils/src/helpers/reset-routes.ts
import type { RouteRecordName, RouteRecordRaw, Router } from 'vue-router';

export function resetStaticRoutes(
  router: Router,
  routes: RouteRecordRaw[],
): void;
```

```ts
// packages/utils/src/helpers/merge-route-modules.ts
interface RouteModuleType {
  default: RouteRecordRaw[];
}

function mergeRouteModules(
  routeModules: Record<string, unknown>,
): RouteRecordRaw[];
```

## Generic traverse helpers (re-exported)

```ts
// @vben-core/shared/utils re-exports
declare function mapTree<T, R>(tree: T[], mapper: (node: T) => R): R[];
declare function filterTree<T>(tree: T[], predicate: (node: T) => boolean): T[];
declare function sortTree<T>(tree: T[], compare: (a: T, b: T) => number): T[];
declare function traverseTreeValues<T, V>(tree: T[], mapper: (node: T) => V): V[];
```

## Strict-mode patterns

### 1. Optional vs. nullable

```ts
// ✅ Good — explicit nullability
function findMenuByPath(list: MenuRecordRaw[], path?: string): MenuRecordRaw | null;

// ❌ Bad — undefined union
function findMenuByPath(list: MenuRecordRaw[], path: string): MenuRecordRaw;
```

### 2. Discriminated input

```ts
// ✅ Good — typed input via union
function mergeRouteModules(
  routeModules: Record<string, unknown>,
): RouteRecordRaw[];

// ❌ Bad — bypass typing
function mergeRouteModules(routeModules: any): any[];
```

### 3. Generics for traversers

```ts
// ✅ Good — generic preserves shape
function mapTree<T, R>(tree: T[], mapper: (node: T) => R): R[];

// ❌ Bad — fixed shape
function mapTree(tree: RouteRecordRaw[], mapper: (node: any) => RouteRecordRaw): RouteRecordRaw[];
```

## TS config

```json
// packages/utils/tsconfig.json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` + `noUnusedLocals`.

## Conventions

- **`import type`** for types-only from `vue-router` etc.
- **Explicit return types** — don't rely on inference for public exports.
- **Generic params** for tree helpers — preserve input shape.
- **`unknown` for opaque input** — `any` is forbidden.
- **No `as` casts** — refactor.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/utils
```

## Forbidden

- ❌ 不要 use `any` in signatures — `unknown` for opaque
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 `as` casts to silence type errors — refactor
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 add `default` exports — break tree-shaking
- ❌ 不要 mutate input arguments — pure functions
- ❌ 不要 return `Promise<void>` from sync helpers — sync only
- ❌ 不要 overload a single helper with incompatible signatures
