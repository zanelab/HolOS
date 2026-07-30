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

## Pinia 状态存储（本应用中使用）

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

## 禁止

- ❌ Don't persist auth tokens in localStorage (XSS).
- ❌ 不要使用 Vuex — 本代码库使用 Pinia。
- ❌ Don't mutate preferences outside the store API (`updatePreferences(...)`).
- ❌ 不要每个功能都创建一个 Pinia store — 跨功能共享状态限到 5 个 store 以内。
- ❌ Don't add Vue 3 `provide`/`inject` keys for data the page itself owns — that's just props.
