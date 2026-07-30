# @vben/preferences Type Safety

> All exports are typed end-to-end. Generics for custom fields.

## Purpose

`@vben/preferences` is the type gateway to the preferences singleton. Every
helper has a precise generic signature so app-level overrides are checked at
compile time, not runtime.

## Public type surface

```ts
// packages/preferences/src/index.ts (verified)
import type {
  CustomPreferencesRecord,
  Preferences,
  PreferencesExtension,
} from '@vben-core/preferences';
import type { DeepPartial } from '@vben-core/typings';

function defineOverridesPreferences(
  preferences: DeepPartial<Preferences>,
): DeepPartial<Preferences>;

function definePreferencesExtension<
  TCustomPreferences extends object = CustomPreferencesRecord,
>(
  extension: PreferencesExtension<TCustomPreferences>,
): PreferencesExtension<TCustomPreferences>;
```

## Real override pattern

```ts
// apps/web-antdv-next/src/preferences.ts
import { defineOverridesPreferences } from '@vben/preferences';

export const overridesPreferences = defineOverridesPreferences({
  app: {
    name: import.meta.env.VITE_APP_TITLE,
    // TS error: 'foo' is not a key of Preferences['app']
    // badProp: 1,
  },
});
```

## Custom extension pattern

```ts
// apps/web-ele/src/preferences-extension.ts
import type { PreferencesExtension } from '@vben/preferences';
import { definePreferencesExtension } from '@vben/preferences';

interface EleCustomPreferences {
  enableVxeTable: boolean;
}

export const extension = definePreferencesExtension<EleCustomPreferences>({
  enableVxeTable: true,
});
```

## Type guideline table

| Pattern | Use |
|---|---|
| `DeepPartial<Preferences>` | nested partial overrides |
| `PreferencesExtension<T>` | add custom fields |
| `CustomPreferencesRecord` | open record for unknown extras |
| `usePreferences()` | returns strongly typed `computed` refs |

## TS config

```json
// packages/preferences/tsconfig.json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` + `noUnusedLocals`.

## Conventions

- **`import type`** for type-only imports (e.g., `Preferences`).
- **`export *`** only for runtime helpers, never for types.
- **Generic parameters** on `definePreferencesExtension` default to
  `CustomPreferencesRecord` for backward compat.
- **No `any`** — every helper's argument is constrained by a public type.
- **Class-level types** are visible only via `preferencesManager` re-export;
  consumers should not depend on the class shape.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/preferences
```

## Forbidden

- ❌ 不要 use `any` for override arguments — `DeepPartial<Preferences>` only
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 `as` casts to silence preference typing errors
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 add `Record<string, any>` for custom prefs — extend the type union
- ❌ 不要 publish `dist/` missing `verbatimModuleSyntax` compliance
- ❌ 不要 extend `Preferences` via namespace augmentation — use extension
