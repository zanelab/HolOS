# @vben/preferences Hook Guidelines

> One public composable: `usePreferences()`. Re-exported from `@vben-core/preferences`.

## Purpose

`@vben/preferences` does not define new composables — it re-exports
`usePreferences()` from `@vben-core/preferences`. The composable wraps the
singleton `preferences` reactive object with `computed` selectors so that
components subscribe only to the slices they care about.

## Verbatim `usePreferences()`

```ts
// packages/@core/preferences/src/use-preferences.ts (verified excerpt)
import { computed } from 'vue';
import { diff } from '@vben-core/shared/utils';

import { preferencesManager } from './preferences';
import { isDarkTheme } from './update-css-variables';

function usePreferences() {
  const preferences = preferencesManager.getPreferences();
  const customPreferences = preferencesManager.getCustomPreferences();
  const diffPreference = computed(() => diff(initialPreferences, preferences));
  const appPreferences = computed(() => preferences.app);
  const shortcutKeysPreferences = computed(() => preferences.shortcutKeys);
  const isDark = computed(() => isDarkTheme(preferences.theme.mode));
  // ...
  return {
    appPreferences,
    diffPreference,
    isDark,
    preferences,
    shortcutKeysPreferences,
    // ...
  };
}
```

## Usage in app

```ts
// apps/web-antdv-next/src/app.vue
import { usePreferences } from '@vben/preferences';

const { isDark } = usePreferences();
watch(() => isDark.value, (dark) => {
  document.documentElement.classList.toggle('dark', dark);
});
```

## Bound action hook

```ts
// apps/web-antdv-next/src/views/preferences/index.vue
import { updatePreferences, usePreferences } from '@vben/preferences';

const { appPreferences } = usePreferences();
const loading = ref(false);

async function handleReset() {
  loading.value = true;
  try {
    await resetPreferences();
    message.success('已重置');
  } finally {
    loading.value = false;
  }
}

function toggleTheme() {
  updatePreferences({
    theme: { mode: isDark.value ? 'light' : 'dark' },
  });
}
```

## Conventions

- **Single composable** — `usePreferences()` is the only public hook.
- **`computed`-wrapped accessors** — never return raw `reactive` slices.
- **Reading is free** — calling `usePreferences()` does not subscribe to
  the whole tree; only accessed `.value` properties trigger subscriptions.
- **No `watchEffect()` inside the composable** — pure derivation.
- **Returns `preferences` raw** for advanced cases (e.g., deep diff views).
- **Side-effect free** — no `onMounted` / `onUnmounted` inside.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Composable | `usePreferences()` | — |
| Computed accessor | `camelCase` (`appPreferences`, `isDark`) | — |
| Mutator | `updatePreferences(DeepPartial<Preferences>)` | — |
| Reset | `resetPreferences()` | — |

## Forbidden

- ❌ 不要 add `useXxx()` beyond the existing `usePreferences()` — re-export only
- ❌ 不要 `watch()` inside `usePreferences()` — pure derivation
- ❌ 不要 use `ref` for derived state — defer to `computed`
- ❌ 不要 wrap `usePreferences` in a `try/catch` — it's sync
- ❌ 不要 return refs that don't depend on `preferences` — wrong layer
- ❌ 不要 call `usePreferences()` outside Vue setup context (it's a composable)
