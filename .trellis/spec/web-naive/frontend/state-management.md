# web-naive State Management

> Pick the simplest container that fits. Don't reach for Pinia first.

## Decision Tree

| Where the state lives | Use |
|---|---|
| One component, one render | `ref()` / `reactive()` |
| One component, deep children | `provide()` / `inject()` |
| Cross-page, persisted | `preferences` store (@vben/preferences) |
| Cross-page, transient | Pinia store (@vben/stores) |
| Server cache | API + `useAsyncResource` |

## Pinia Stores (canonical 3)

```ts
import { useAccessStore } from '@vben/stores';
const accessStore = useAccessStore();
accessStore.setAccessMenus(menus);
accessStore.setIsAccessChecked(true);
```

- **useAccessStore** — tokens, access routes, access flags
- **useAuthStore** — login / logout / token expiry modal
- **useUserStore** — current user, avatar, homePath

## preferences — the only persisted state

```ts
// src/preferences.ts
export const overridesPreferences = defineOverridesPreferences({
  app: {
    name: import.meta.env.VITE_APP_TITLE,
    defaultHomePath: '/dashboard',  // can override
  },
});
```

Persisted in `localStorage` 键 `vben-<namespace>-<version>-<env>-preferences`.

## naive-ui 状态差异

Ui 框架 specific state:
```ts
// Naive UI - useLoadingBar
import { useLoadingBar } from 'naive-ui';
const loadingBar = useLoadingBar();
loadingBar.start(); // 全局 loading
loadingBar.finish();

// Element Plus - ElMessage / ElMessageBox
import { ElMessage } from 'element-plus';
ElMessage.success('Saved');
```

These 应该包装进 `useToast()` / `useLoading()` composables, not directly 用。

## Forbidden

- ❌ Don't persist auth tokens in localStorage (XSS risk)
- ❌ Don't use Vuex — Pinia only
- ❌ Don't mutate preferences outside the store API
- ❌ Don't add new Pinia stores per feature — keep shared stores ≤ 5
- ❌ Don't pollute Pinia with each-flavor-specific state (UI state belongs in adapter)
