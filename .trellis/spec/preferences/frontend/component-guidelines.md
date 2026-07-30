# @vben/preferences Component Guidelines

> No Vue components in this package — pure functions + types.

## Purpose

`@vben/preferences` does not ship SFCs. Components live in
`@vben-core/preferences` (the `update-css-variables.ts` utility), in
`apps/web-*/src/views/preferences/**`, and in the `usePreferences()` composable
that returns reactive `computed` refs.

## Where the reactive UI lives

`usePreferences()` (re-exported from `@vben-core/preferences`) returns a
set of computed refs that components subscribe to:

```ts
// apps/web-antdv-next/src/app.vue (real)
import { preferences, usePreferences } from '@vben/preferences';

const { isDark } = usePreferences();
const { tokens } = useAntdDesignTokens();

const tokenTheme = computed(() => {
  const algorithm = isDark.value
    ? [theme.darkAlgorithm]
    : [theme.defaultAlgorithm];
  if (preferences.app.compact) {
    algorithm.push(theme.compactAlgorithm);
  }
  return { algorithm, token: tokens };
});
```

## Real Preferences Drawer (app-side)

Apps mount a preferences drawer that calls `updatePreferences` directly:

```vue
<!-- apps/web-antdv-next/src/layouts/basic.vue (real pattern) -->
<script setup lang="ts">
import { usePreferences } from '@vben/preferences';

const { globalSearchShortcut } = usePreferences();

function toggleSearch() {
  updatePreferences({
    shortcutKeys: {
      globalSearch: !globalSearchShortcut.value,
    },
  });
}
</script>

<template>
  <Button @click="toggleSearch">
    {{ globalSearchShortcut ? 'ON' : 'OFF' }}
  </Button>
</template>
```

## Component conventions

- **Components read `usePreferences()`** for reactive access — never read
  `preferences` directly in templates (loses reactivity).
- **Mutations via `updatePreferences(partial)`** — partial is `DeepPartial<Preferences>`.
- **Reset via `resetPreferences()`** to roll back to last saved snapshot.
- **No `<style>` overrides for theme** — use design tokens + `updatePreferences`.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Composable return | `usePreferences()` | `usePreferences()` |
| Field path | `preferences.<namespace>.<field>` | `preferences.theme.mode` |
| Override helper | `defineOverridesPreferences(...)` | `defineOverridesPreferences({ app: { name: 'X' } })` |
| Custom extension | `definePreferencesExtension<TCustom>(...)` | — |

## Forbidden

- ❌ 不要写 `preferences.xxx = '...'` 直接 mutation — use `updatePreferences`
- ❌ 不要 read `preferences` in `setup()` and destructure — breaks reactivity
- ❌ 不要 put per-page UI state in `preferences` — use component-local state
- ❌ 不要 write multi-level `.deep.value` traversal — use computed wrappers
- ❌ 不要 override theme colours via inline style — use `updatePreferences`
- ❌ 不要 import `defineOverridesPreferences` outside `preferences.ts` (app)
- ❌ 不要 wrap `usePreferences` in `try/catch` — it's sync
