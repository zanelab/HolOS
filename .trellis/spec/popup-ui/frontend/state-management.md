# popup-ui — PLACEHOLDER SPEC

**Expected package:** `@vben-core/popup-ui` — Popup wrappers — `VbenModal`, `VbenDrawer`, `VbenDropdown`, `VbenPopover`, `VbenTooltip`. Wrap shadcn-vue + naive-ui popups with Vben preferences.

> ⚠️ **PLACEHOLDER DOCS** — This package does **not** exist in the current
> workspace. The structure, conventions, and code examples below are
> best-guess projections based on the upstream `vben v5.7.0` monorepo
> (`vbenjs/vben-admin-monorepo`) and the role this package plays
> in a real vben app. **Replace this file with real content when (and
> only when) the corresponding `packages/popup-ui/`
> directory lands upstream.**

Do **not** implement against this placeholder — code that imports from
`@vben-core/popup-ui` will fail to typecheck.
## Where state lives in vben

| Lifetime | Mechanism | Package |
|---|---|---|
| Component-local | `ref()` / `reactive()` / `shallowRef()` | inside `<script setup>` |
| Cross-page, persisted | preferences store | `@vben/preferences` |
| Cross-page, transient | Pinia store | `@vben/stores` |
| Server cache | `@vben/request` + `useXxx` composable | apps |
| App-wide singletons | `provide` / `inject` at the layout root | layouts |

## Decision tree for `@vben-core/popup-ui` role `popups`

```
Need state?
  ├─ Only inside a component  →  ref() / reactive()
  ├─ Shared by 2+ components   →  Pinia store (@vben/stores)
  ├─ Persisted across reloads  →  preferences store (@vben/preferences)
  ├─ Derived from above        →  computed() inside composable
  └─ Server source of truth    →  @vben/request + useResource pattern
```

## Example: Pinia store (Setup-style)

```ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

interface XItem { id: string; name: string; }

export const useXStore = defineStore('x', () => {
  const list = ref<XItem[]>([]);
  const loading = ref(false);

  async function load() {
    loading.value = true;
    try { list.value = await fetchX(); }
    finally { loading.value = false; }
  }

  function reset() { list.value = []; }

  return { list, loading, load, reset };
});
```

## Example: preferences-backed reactive value

```ts
import { usePreferences } from '@vben/preferences';
import { computed } from 'vue';

export function useCurrentLayout() {
  const prefs = usePreferences();
  return computed(() => prefs.app.layout);
}
```

## Example: stateless lib function (preferred for `@vben-core/popup-ui`)

```ts
import type { AccessMode } from './types';

export function evaluateAccess(
  mode: AccessMode,
  roles: readonly string[],
  resource: string,
): boolean {
  // pure — no Pinia, no ref — caller wraps in computed
  if (mode === 'public') return true;
  return roles.includes(resource);
}
```

## SSR / hydration

- Stores must not capture `window` / `document` at module top-level.
- Defer `localStorage` access into the preferences store's
  `onHydrated` callback.

## Forbidden

- ❌ Don't use Vuex — the monorepo is Pinia-only.
- ❌ Don't persist auth tokens to `localStorage` directly — go through
  `@vben/stores` and the request interceptor.
- ❌ Don't mutate preferences outside the store's actions/mutations.
- ❌ Don't share a single `ref()` across composables — wrap in a store.
- ❌ Don't call `useStore()` at module top-level (outside `setup()`).
- ❌ Don't put `fetch` calls in `getters` — keep them in actions.
