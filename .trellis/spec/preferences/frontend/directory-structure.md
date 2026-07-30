# @vben/preferences Directory Structure

> Real layout for `packages/preferences/`. Source verified 2026-07-30.

## Purpose

`@vben/preferences` is the workspace's app-preferences **adapter**. It re-exports
the core `PreferenceManager` from `@vben-core/preferences` and adds two
app-facing helpers: `defineOverridesPreferences` and `definePreferencesExtension`.
Apps call these at bootstrap to merge per-app overrides into the global
preferences without forking the core defaults.

## 目录树 (verified from `packages/preferences/`)

```
@vben/preferences/                  # workspace: packages/preferences/
├── package.json                    # name "@vben/preferences" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
└── src/
    └── index.ts                    # public barrel — defineOverridesPreferences + re-exports
```

Single-file package. Everything delegates to `@vben-core/preferences`.

## Real source (verified)

```ts
// packages/preferences/src/index.ts
import type {
  CustomPreferencesRecord,
  Preferences,
  PreferencesExtension,
} from '@vben-core/preferences';
import type { DeepPartial } from '@vben-core/typings';

/**
 * 如果你想所有的app都使用相同的默认偏好设置，你可以在这里定义
 * 而不是去修改 @vben-core/preferences 中的默认偏好设置
 * @param preferences
 * @returns
 */
function defineOverridesPreferences(preferences: DeepPartial<Preferences>) {
  return preferences;
}

function definePreferencesExtension<
  TCustomPreferences extends object = CustomPreferencesRecord,
>(extension: PreferencesExtension<TCustomPreferences>) {
  return extension;
}

export { defineOverridesPreferences, definePreferencesExtension };
export * from '@vben-core/preferences';
```

## Re-exported surface

| Symbol | Source | Purpose |
|---|---|---|
| `initPreferences` | `@vben-core/preferences` | bootstrap side-effect: loads cache |
| `preferences` | `@vben-core/preferences` | reactive current snapshot |
| `updatePreferences` | `@vben-core/preferences` | mutate one field |
| `resetPreferences` | `@vben-core/preferences` | reload defaults |
| `usePreferences()` | `@vben-core/preferences` | composable wrappers |
| `defineOverridesPreferences` | this package | merge per-app defaults |
| `definePreferencesExtension` | this package | add custom fields |

## Conventions

- **Single barrel** at `src/index.ts` — no other source files.
- **Pure re-exports** of the core package; type-only passthrough via `export *`.
- **No IO** in this package — `initPreferences` is forwarded as-is.
- **No Pinia / Vue runtime** outside `preferences.ts` (which lives in `@core`).
- **Tree-shake friendly** — both helpers are individually named exports.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Public helper | `defineXxx...` | `defineOverridesPreferences` |
| File | `index.ts` (single barrel) | — |
| Type passthrough | `export * from '@vben-core/preferences'` | — |

## Forbidden

- ❌ 不要 add Vue components / Pinia stores — only types + helper functions
- ❌ 不要 bypass core PreferenceManager logic — `initPreferences` does the work
- ❌ 不要 bypass `defineOverridesPreferences` for default merging — that's its job
- ❌ 不要 mutating `preferences` object directly — use `updatePreferences`
- ❌ 不要 place business defaults in core `@vben-core/preferences` — use overrides
- ❌ 不要 import `@vben/constants` / `@vben/stores` here — pure passthrough
