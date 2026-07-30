# @vben/stores Component Guidelines

> No Vue SFCs in this package. Stores are exposed via Pinia.

## Purpose

`@vben/stores` does not ship Vue components. App components consume the
stores via `useXxxStore()` and `storeToRefs()`. This file documents the
binding patterns between components and `@vben/stores`.

## Recommended: `storeToRefs`

```vue
<!-- apps/web-antdv-next/src/layouts/basic.vue (real pattern) -->
<script setup lang="ts">
import { storeToRefs } from 'pinia';

import { useAccessStore } from '@vben/stores';

const accessStore = useAccessStore();
const { accessToken, accessCodes } = storeToRefs(accessStore);
</script>

<template>
  <div v-if="accessToken">
    <span>{{ accessCodes.length }} codes</span>
  </div>
</template>
```

`storeToRefs` keeps the bindings reactive — destructuring the store directly
breaks reactivity for non-ref state.

## Action calls

```vue
<script setup lang="ts">
import { useUserStore } from '@vben/stores';

const userStore = useUserStore();

function logout() {
  userStore.setUserInfo(null);
}
</script>
```

## When to use computed vs. storeToRefs

```vue
<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useAccessStore } from '@vben/stores';

const accessStore = useAccessStore();
const { accessMenus } = storeToRefs(accessStore);

// Derived value — computed, not stored as state
const accessiblePaths = computed(() =>
  accessMenus.value.map((m) => m.path),
);
</script>
```

## Real action with payload

```ts
// apps/web-antdv-next/src/store/auth.ts
import { useAccessStore, useUserStore } from '@vben/stores';

export const useAuthStore = defineStore('auth', () => {
  const accessStore = useAccessStore();
  const userStore = useUserStore();

  async function authLogin(params: Recordable<any>) {
    const { accessToken } = await loginApi(params);
    if (accessToken) {
      accessStore.setAccessToken(accessToken);
      const [userInfo, codes] = await Promise.all([
        fetchUserInfo(),
        getAccessCodesApi(),
      ]);
      accessStore.setAccessCodes(codes);
    }
  }
  return { authLogin };
});
```

## Conventions

- **`useXxxStore()` inside `<script setup>`** — calling it outside a Vue
  context throws.
- **`storeToRefs()` for state** — actions are bound directly on the store.
- **No `$patch` for top-level mutations** — use the typed `set*` actions.
- **No component-local mirror of store state** — single source.
- **App store modules** live in `apps/web-*/src/store/<name>.ts` and use
  `defineStore(<id>, setupFn)`.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Store name | `useXxxStore` | `useAccessStore` |
| Pinia id | `core-<scope>` / `auth` (app) | `core-access`, `auth` |
| Action setter | `setXxx(value)` | `setAccessToken(token)` |
| Action getter | `findXxx(args)` | `findMenuByPath(path)` |

## Forbidden

- ❌ 不要 destructure store without `storeToRefs()` — loses reactivity
- ❌ 不要 call `useXxxStore()` outside Vue setup — throws
- ❌ 不要 use `store.$patch` for complex merges — use a typed action
- ❌ 不要 read `.value` on a `storeToRefs` return without re-exporting
- ❌ 不要 define a Pinia plugin in components — `@vben/stores` configures it
- ❌ 不要 bind entire store to a template — pick fields via `storeToRefs`
- ❌ 不要 create a circular reference between stores — use events / props
