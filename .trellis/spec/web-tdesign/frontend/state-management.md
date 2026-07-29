# @vben/web-tdesign State Management

> Pick the **simplest** state container that fits. Don't reach for Pinia first.

## Decision Tree

| Where the state lives | Use |
|---|---|
| One component, one render | `ref()` / `reactive()` |
| One component, deep children | `provide()` / `inject()` |
| Cross-page but app-global, persisted | `preferences` store (`@vben/preferences`) |
| Cross-page, transient | Pinia store |
| Server cache | API + `useAsyncResource` (see hook-guidelines.md) |
| Cross-tab sync | localStorage with `@vueuse/core` `useStorage` |

## Pinia Stores (used in this app)

- **`useAccessStore`** — tokens, access routes, access flags
  ```ts
  // real usage (from src/router/access.ts)
  import { useAccessStore } from '@vben/stores';
  const accessStore = useAccessStore();
  accessStore.setAccessMenus(menus);
  accessStore.setIsAccessChecked(true);
  ```
- **`useAuthStore`** — login / register / logout; token expiry modal
- **`useUserStore`** — current user info (`userInfo`, `avatar`, `homePath`)

## `preferences` Store — the only **persisted** state

```ts
// src/preferences.ts (real pattern from this app)
export const overridesPreferences = defineOverridesPreferences({
  app: { name: import.meta.env.VITE_APP_TITLE },
});
```

Persisted under localStorage key `vben-web-tdesign-5.7.0-dev-preferences`.

## Forbidden

- ❌ Don't persist auth tokens in localStorage (XSS).
- ❌ Don't use Vuex — this codebase uses Pinia.
- ❌ Don't mutate preferences outside the store API (`updatePreferences(...)`).
- ❌ Don't create a new Pinia store per feature — keep cross-feature shared state to ≤ 5 stores.
- ❌ Don't add Vue 3 `provide`/`inject` keys for data the page itself owns — that's just props.
