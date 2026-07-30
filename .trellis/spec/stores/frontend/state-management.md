# @vben/stores State Management

> Pinia is the only state layer. Stores are split by concern.

## Purpose

`@vben/stores` owns the shared Pinia instance via `initStores()`, the SecureLS
persistence, and four core stores. Each store holds a single concern: tokens
(`access`), user info (`user`), tab history (`tabbar`), and timezone
(`timezone`). App-specific stores (`auth`, `demo-progress`) live elsewhere.

## Core stores

```ts
// packages/stores/src/modules/access.ts (verified excerpt)
export const useAccessStore = defineStore('core-access', {
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
  actions: {
    setAccessToken(token: AccessToken) { this.accessToken = token; },
    setAccessCodes(codes: string[]) { this.accessCodes = codes; },
    getMenuByPath(path: string) { /* tree walk */ },
    lockScreen(password: string) { /* ... */ },
    unlockScreen() { /* ... */ },
  },
  persist: {
    pick: ['accessToken', 'refreshToken', 'accessCodes', 'isLockScreen', 'lockScreenPassword'],
  },
});
```

## Tabbar store (more complex)

```ts
// packages/stores/src/modules/tabbar.ts (real, ~770 lines)
export const useTabbarStore = defineStore('core-tabbar', {
  state: (): TabbarState => ({
    cachedRoutes: new Map(),
    cachedTabs: new Set(),
    dragEndIndex: 0,
    excludeCachedTabs: new Set(),
    menuList: [],
    tabs: [],
    visitHistory: createStack<string>(),
  }),
  actions: {
    addTab(routeTab: TabDefinition) { /* ... */ },
    closeTab(tab: TabDefinition, router: Router) { /* ... */ },
    refresh(router: Router | string) { /* ... */ },
  },
  getters: { /* derived */ },
});
```

## Setup-style store

```ts
// packages/stores/src/modules/timezone.ts (real)
export const useTimezoneStore = defineStore(
  'core-timezone',
  () => {
    const timezoneRef = ref(getCurrentTimezone());
    async function setTimezone(tz: string) {
      timezoneRef.value = tz;
      setCurrentTimezone(tz);
    }
    return { setTimezone, timezone: timezoneRef };
  },
  { persist: { pick: ['timezone'] } },
);
```

## Persistence contract

`createPersistedState` from `pinia-plugin-persistedstate` is loaded **only**
inside `initStores()` (dynamic import) and the storage adapter is **SecureLS**
in prod and **localStorage** in dev:

```ts
pinia.use(
  createPersistedState({
    key: (storeKey) => `${namespace}-${storeKey}`,
    storage: import.meta.env.DEV
      ? localStorage
      : {
          getItem(key) { return ls.get(key); },
          setItem(key, value) { ls.set(key, value); },
        },
  }),
);
```

## State surface map

| Store | Pinia id | Persistence | Notes |
|---|---|---|---|
| `useAccessStore` | `core-access` | `pick: [tokens, codes, lock]` | Sensitive — SecureLS in prod |
| `useUserStore` | `core-user` | none | Ephemeral |
| `useTabbarStore` | `core-tabbar` | none | In-memory only |
| `useTimezoneStore` | `core-timezone` | `pick: ['timezone']` | Single field |

## Conventions

- **Pinia is the only state layer** — no `useState`/`reactive`/`provide` flows.
- **One concern per store** — don't merge `user` + `preferences` into one.
- **Persistence declared via `persist: { pick: [...] }`** — opt-in.
- **Reset is per-store** (`store.$reset()`) and global (`resetAllStores()`).
- **No cross-store constructors** — if A needs B, call `useBStore()` lazily.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Store id | `core-<scope>` | `core-access` |
| Action | `setXxx` / `findXxx` / `closeXxx` | `setAccessToken` |
| Getter | `getXxx` | `getMenuByPath` (action, not getter) |
| Persistent field | listed in `persist.pick` | `accessToken` |

## Forbidden

- ❌ 不要 create a store with `any` state — always typed `state()`
- ❌ 不要 put `localStorage.setItem` in a store action — use `persist`
- ❌ 不要 persist `userInfo` — fetch fresh on app boot
- ❌ 不要 combine two concerns in one store
- ❌ 不要 call `useOtherStore()` in `setup()` of a store — lazy-init only
- ❌ 不要 use `store.$patch` for complex object merges — write a typed action
- ❌ 不要 define stores globally — Pinia instances are per-app
