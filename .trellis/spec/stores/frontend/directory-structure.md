# @vben/stores Directory Structure

> Real layout for `packages/stores/`. Source verified 2026-07-30.

## Purpose

`@vben/stores` is the workspace's shared Pinia state. It owns the Pinia
init plugin (`initStores`), the SecureLS-backed persistence layer, and a
small set of core stores (`access`, `tabbar`, `timezone`, `user`) reused by
every web-* app. App-level stores (`auth`, `demo`) live in
`apps/web-*/src/store/` instead.

## 目录树 (verified from `packages/stores/`)

```
@vben/stores/                       # workspace: packages/stores/
├── package.json                    # name "@vben/stores" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
├── index.ts                        # public barrel — re-exports + pinia re-exports
├── setup.ts                        # initStores + resetAllStores + SecureLS
└── modules/
    ├── index.ts                    # re-exports all stores
    ├── access.ts                   # useAccessStore (options-style)
    ├── access.test.ts              # vitest
    ├── tabbar.ts                   # useTabbarStore (options-style)
    ├── tabbar.test.ts
    ├── user.ts                     # useUserStore (options-style)
    ├── user.test.ts
    └── timezone.ts                 # useTimezoneStore (setup-style)
```

## Real source excerpts

```ts
// packages/stores/src/index.ts
export * from './modules';
export * from './setup';
export { defineStore, storeToRefs } from 'pinia';
```

```ts
// packages/stores/src/setup.ts (verified)
export async function initStores(app: App, options: InitStoreOptions) {
  const { createPersistedState } = await import('pinia-plugin-persistedstate');
  pinia = createPinia();
  const { namespace } = options;
  const ls = new SecureLSConstructor({
    encodingType: 'aes',
    encryptionSecret: import.meta.env.VITE_APP_STORE_SECURE_KEY,
    isCompression: true,
    metaKey: `${namespace}-secure-meta`,
  });
  pinia.use(
    createPersistedState({
      key: (storeKey) => `${namespace}-${storeKey}`,
      storage: import.meta.env.DEV ? localStorage : { /* secure ls */ },
    }),
  );
  app.use(pinia);
  return pinia;
}
```

## Conventions

- **One module file per store** — `access.ts` ↔ `useAccessStore`.
- **Mixed styles allowed** — most core stores are Options-style; `timezone` is
  setup-style. Choose per module's reactivity shape.
- **Hot Module Replacement** via `acceptHMRUpdate(useStore, hot)` at file end.
- **App-level namespace** — `${namespace}-${storeKey}` prefixes every persisted key.
- **Tests are colocated** — `*.test.ts` next to source.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Store name | `useXxxStore` | `useAccessStore` |
| Pinia id | `core-<scope>` | `core-access`, `core-tabbar` |
| Module file | `<scope>.ts` | `access.ts`, `user.ts` |
| Test file | `<scope>.test.ts` | `access.test.ts` |

## Forbidden

- ❌ 不要 put app-specific stores in this package — apps own those
- ❌ 不要 bypass `initStores` for app Pinia creation — uses a single instance
- ❌ 不要 hardcode `namespace` — passed from app `main.ts`
- ❌ 不要 import stores via deep paths — use the public barrel
- ❌ 不要 add Pinia stores besides `access`, `tabbar`, `user`, `timezone` here
- ❌ 不要 skip `acceptHMRUpdate` — HMR breaks without it
