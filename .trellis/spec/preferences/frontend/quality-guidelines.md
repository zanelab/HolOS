# @vben/preferences Quality Guidelines

> Single barrel, type-safe helpers, no runtime surprises.

## Purpose

`@vben/preferences` is a thin adapter. The quality bar is "every export is
typed, every helper is generic, no IO, no surprise side effects."

## TS file style

```ts
// packages/preferences/src/index.ts (real)
import type {
  CustomPreferencesRecord,
  Preferences,
  PreferencesExtension,
} from '@vben-core/preferences';
import type { DeepPartial } from '@vben-core/typings';

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

- **2-space indent**
- **Single quotes**
- **No semicolons**
- **Trailing newline**
- **`import type`** for type-only imports
- **Generics** on `definePreferencesExtension` for custom field types

## Real usage pattern

```ts
// apps/web-antdv-next/src/preferences.ts
import { defineOverridesPreferences } from '@vben/preferences';

export const overridesPreferences = defineOverridesPreferences({
  app: {
    name: import.meta.env.VITE_APP_TITLE,
  },
});
```

## Conventions

- **Single barrel** — `src/index.ts` is the only file.
- **Type-only imports** — `import type { ... }` for `Preferences`.
- **No business defaults in core** — apps override via `defineOverridesPreferences`.
- **No IO** — `initPreferences` is forwarded, not redefined.
- **No Vue runtime** — `preferences` is the only object component code touches.
- **Tree-shake friendly** — named exports only.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Helper | `defineOverridesPreferences` / `definePreferencesExtension` | — |
| Type | `Preferences`, `CustomPreferencesRecord`, `PreferencesExtension` | — |
| File | `src/index.ts` | — |
| Generic param | `TCustomPreferences` | `<TCustomPreferences extends object = CustomPreferencesRecord>` |

## Linting & pre-commit

- ESLint flat config
- OxLint
- OxFmt (auto-format)
- `pnpm typecheck` includes `@vben/preferences`

## Forbidden

- ❌ 不要 add `.ts` / `.vue` files beyond `src/index.ts` — single barrel
- ❌ 不要 import `vue` runtime here — passthrough only
- ❌ 不要 add `console.log` for debugging — remove before commit
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 override `preferences` with `Object.assign` — use `updatePreferences`
- ❌ 不要 place per-app default UI config in core
- ❌ 不要 add `as any` to silence preference typing
