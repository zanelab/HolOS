# @vben/preferences State Management

> Reactive state is the singleton `preferences` object — owned by core.

## Purpose

`@vben/preferences` does not own state. The single reactive surface is
`preferences` (a `reactive<Preferences>` object) hosted by
`@vben-core/preferences/PreferenceManager`. This package only re-exports the
manager's API and the helper functions `defineOverridesPreferences` /
`definePreferencesExtension`.

## The singleton

```ts
// packages/@core/preferences/src/preferences.ts (verified)
class PreferenceManager {
  private state: Preferences;
  private initialPreferences: Preferences = defaultPreferences;
  private isInitialized = false;
  private customState = reactive<CustomPreferencesRecord>({});

  constructor() {
    this.state = reactive<Preferences>({ ...defaultPreferences });
    this.debouncedSave = useDebounceFn(() => this.saveToCache(), 150);
  }
  // ...
}
```

It's a class with a **module-level singleton** (`preferencesManager`) and
mutations go through a debounced save (150ms) to localStorage.

## Mutations

```ts
// apps/web-antdv-next/src/views/preferences/preferences-button.vue (real)
import { updatePreferences } from '@vben/preferences';

function setSidebarCollapsed(collapsed: boolean) {
  updatePreferences({
    sidebar: { collapsed },
  });
}
```

`updatePreferences(partial)` merges nested with `vueuse`'s `merge` and triggers
`debouncedSave()`.

## Read flow

```ts
// apps/web-antdv-next/src/app.vue
import { preferences } from '@vben/preferences';
import { watch } from 'vue';

watch(
  () => preferences.theme.mode,
  (mode) => {
    document.documentElement.dataset.theme = mode;
  },
);
```

Reading `preferences.theme.mode` is a reactive read — Vue tracks it.

## State surface map

| Surface | Type | Owned by |
|---|---|---|
| `preferences` | `reactive<Preferences>` | `@vben-core/preferences` |
| `customPreferences` | `reactive<CustomPreferencesRecord>` | `@vben-core/preferences` |
| `preferencesManager` | `PreferenceManager` class | `@vben-core/preferences` |
| `initPreferences` | async bootstrap fn | `@vben-core/preferences` |
| `StorageManager` | cache abstraction | `@vben-core/shared/cache` |

## Conventions

- **Single source of truth** — only `preferencesManager` mutates state.
- **Debounced persistence** — `useDebounceFn(save, 150)`.
- **Reactive reads** — `preferences.app.x` is a tracked dependency.
- **No new state in this package** — pure passthrough.
- **Async init** — `initPreferences()` must be awaited before `app.use(router)`.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Manager | `preferencesManager` | — |
| Snapshot | `preferences` (re-exported const) | `import { preferences } from '@vben/preferences'` |
| Helper | `defineOverridesPreferences` / `definePreferencesExtension` | — |
| Reset | `resetPreferences()` | — |

## Forbidden

- ❌ 不要 create a Pinia store for preferences — use the singleton
- ❌ 不要 mutate `preferences.theme.mode = 'dark'` directly — call `updatePreferences`
- ❌ 不要 write to `localStorage` directly — manager handles persistence
- ❌ 不要 hold local copy of preferences — read from the singleton
- ❌ 不要 make `initPreferences` synchronous — async only
- ❌ 不要 split preferences across multiple stores — single source of truth
