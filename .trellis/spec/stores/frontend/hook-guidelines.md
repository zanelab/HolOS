# @vben/stores Hook Guidelines

> One Pinia factory per store. No `useXxx` composables wrapping store state.

## Purpose

`@vben/stores` does not define its own composables — Pinia composables
**are** the binding between components and store state. App-level
stateful hooks (e.g., `useTable`, `useForm`) live in `@vben/hooks` or
component-local code, not here.

## Real Options-style store

```ts
// packages/stores/src/modules/user.ts (verified)
import { acceptHMRUpdate, defineStore } from 'pinia';

interface AccessState {
  userInfo: BasicUserInfo | null;
  userRoles: string[];
}

export const useUserStore = defineStore('core-user', {
  actions: {
    setUserInfo(userInfo: BasicUserInfo | null) {
      this.userInfo = userInfo;
      const roles = userInfo?.roles ?? [];
      this.setUserRoles(roles);
    },
    setUserRoles(roles: string[]) {
      this.userRoles = roles;
    },
  },
  state: (): AccessState => ({
    userInfo: null,
    userRoles: [],
  }),
});

const hot = import.meta.hot;
if (hot) {
  hot.accept(acceptHMRUpdate(useUserStore, hot));
}
```

## Real setup-style store

```ts
// packages/stores/src/modules/timezone.ts (verified)
export const useTimezoneStore = defineStore(
  'core-timezone',
  () => {
    const timezoneRef = ref(getCurrentTimezone());

    async function setTimezone(timezone: string) {
      const handler = getTimezoneHandler();
      await handler.setTimezone?.(timezone);
      timezoneRef.value = timezone;
      setCurrentTimezone(timezone);
    }
    return { setTimezone, timezone: timezoneRef };
  },
  { persist: { pick: ['timezone'] } },
);
```

## Initialisation hook

```ts
// packages/stores/src/setup.ts
export async function initStores(app: App, options: InitStoreOptions) {
  const { createPersistedState } = await import('pinia-plugin-persistedstate');
  pinia = createPinia();
  const { namespace } = options;
  // ...
  app.use(pinia);
  return pinia;
}
```

App calls `await initStores(app, { namespace })` once in `bootstrap.ts`.

## Conventions

- **One `useXxxStore` per module file** — colocated definition.
- **Options API preferred** for state-heavy stores (typed `state()`,
  enumerable `actions`).
- **Setup API for derived/reactive-only stores** (e.g., `timezone`).
- **`acceptHMRUpdate` at end of file** — Vite HMR contract.
- **Async init via `initStores`** — never `createPinia()` from app code.
- **`resetAllStores()`** is the canonical "logout" reset.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Pinia hook | `useXxxStore` | `useAccessStore` |
| Pinia id | `core-<scope>` | `core-access` |
| Action | `setXxx` / `findXxx` / `closeXxx` | `setAccessToken` |
| Init | `initStores(app, { namespace })` | — |

## Forbidden

- ❌ 不要 add `useXxx` composables outside `defineStore` — Pinia is the hook
- ❌ 不要 define `ref` outside `setup()`-style stores — wrap in `defineStore`
- ❌ 不要 skip `acceptHMRUpdate` — HMR breaks in dev
- ❌ 不要 call `initStores` twice — second install is a no-op and leaks
- ❌ 不要 call `useUserStore()` at module top-level — needs Pinia active
- ❌ 不要 bundle app-specific stores inside this package — apps own those
- ❌ 不要 use Pinia `getActivePinia()` directly — use `storeToRefs`
