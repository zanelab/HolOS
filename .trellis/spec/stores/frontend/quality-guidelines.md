# @vben/stores Quality Guidelines

> Pinia strictness, SecureLS persistence, typed state.

## Purpose

`@vben/stores` is the shared state backbone. The quality bar is: every
store is fully typed, persistence is opt-in per field, no silent side
effects outside the plugin, and HMR works in dev.

## TS file style

```ts
// packages/stores/src/modules/access.ts (real)
import type { RouteRecordRaw } from 'vue-router';
import type { MenuRecordRaw } from '@vben-core/typings';

import { acceptHMRUpdate, defineStore } from 'pinia';

type AccessToken = null | string;

interface AccessState {
  accessCodes: string[];
  accessMenus: MenuRecordRaw[];
  accessRoutes: RouteRecordRaw[];
  accessToken: AccessToken;
  isAccessChecked: boolean;
  isLockScreen: boolean;
  lockScreenPassword?: string;
  loginExpired: boolean;
  refreshToken: AccessToken;
}

export const useAccessStore = defineStore('core-access', {
  actions: {
    setAccessMenus(menus: MenuRecordRaw[]) { this.accessMenus = menus; },
    setAccessRoutes(routes: RouteRecordRaw[]) { this.accessRoutes = routes; },
  },
  persist: {
    pick: ['accessToken', 'refreshToken', 'accessCodes', 'isLockScreen', 'lockScreenPassword'],
  },
  state: (): AccessState => ({
    accessCodes: [],
    accessMenus: [],
    accessRoutes: [],
    accessToken: null,
    isAccessChecked: false,
    isLockScreen: false,
    lockScreenPassword: undefined,
    loginExpired: false,
    refreshToken: null,
  }),
});

const hot = import.meta.hot;
if (hot) {
  hot.accept(acceptHMRUpdate(useAccessStore, hot));
}
```

- **2-space indent**
- **Single quotes**
- **No semicolons**
- **Trailing newline**
- **`import type`** for type-only imports
- **`interface` for state shape** — `state(): MyState => ({ ... })`
- **Pinia id starts with `core-`** in this package

## HMR contract

At the end of every store file:

```ts
const hot = import.meta.hot;
if (hot) {
  hot.accept(acceptHMRUpdate(useXxxStore, hot));
}
```

## Persistence contract

```ts
persist: {
  pick: ['accessToken', 'refreshToken', 'accessCodes', 'isLockScreen', 'lockScreenPassword'],
}
```

- **Always explicit** — no `persist: true` (full state).
- **Pick only stable fields** — never `userInfo` (live-fetched).
- **No sensitive data outside the pick list** — SecureLS is keyed on app.

## Conventions

- **Per-store ts file** with `useXxxStore` as the only export.
- **State per concern** — avoid multi-domain stores.
- **Action names** — `setXxx`, `addXxx`, `closeXxx`, `resetXxx`, `findXxx`.
- **No getters for async** — use plain functions.
- **No `console.log`** in actions — debug via Pinia devtools.
- **Vue devtools** support — declare `defineStore` with string id.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Store id | `core-<scope>` | `core-access` |
| Action | `set<Field>` | `setAccessToken` |
| Pinia hook | `useXxxStore` | `useAccessStore` |
| Test file | `<scope>.test.ts` | `access.test.ts` |

## Linting & pre-commit

- ESLint flat config
- OxLint
- OxFmt
- Vitest (unit tests colocated)
- `pnpm typecheck` includes `@vben/stores`

## Forbidden

- ❌ 不要 add `console.log` to a store action — use devtools
- ❌ 不要 use `as any` for state shape — extend the interface
- ❌ 不要 write `persist: true` — be explicit with `pick`
- ❌ 不要 skip `acceptHMRUpdate` — dev HMR breaks
- ❌ 不要 call `useUserStore()` at module top-level (needs Pinia active)
- ❌ 不要 mutate `state` directly from outside — use actions
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 return promises from getters — actions only
