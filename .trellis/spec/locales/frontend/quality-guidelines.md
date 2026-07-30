# @vben/locales Quality Guidelines

> Tree-shake friendly, JSON-driven, type-checked via `SupportedLanguagesType`.

## Purpose

`@vben/locales` is a leaf package: it must be deterministic, locale-aware
without surprises, and never bundle all languages into the main chunk. The
quality bar is "translations load lazily, missing keys warn loudly, types
catch typos at compile time."

## JSON file style

```json
// packages/locales/src/langs/en-US/common.json
{
  "add": "Add",
  "confirm": "Confirm",
  "cancel": "Cancel",
  "loading": "Loading",
  "search": "Search",
  "reset": "Reset"
}
```

- **2-space indent** for JSON
- **No trailing commas**
- **Double quotes** for keys and string values
- **Stable key order** — alphabetise or group by domain
- **No comments** — JSON forbids them; use a sibling `*.d.ts` if needed

## TS file style

```ts
// packages/locales/src/i18n.ts (real)
export type SupportedLanguagesType = 'en-US' | 'zh-CN';

export interface LocaleSetupOptions {
  defaultLocale?: SupportedLanguagesType;
  loadMessages?: LoadMessageFn;
  missingWarn?: boolean;
}
```

- **2-space indent** for TS
- **Single quotes** for strings
- **Trailing newline**
- **No semicolons** (matches root config)
- **`import type`** for type-only imports

## Real loader (verified)

```ts
// packages/locales/src/i18n.ts (verified, abridged)
const modules = import.meta.glob('./langs/**/*.json');

const localesMap = loadLocalesMapFromDir(
  /\.\/langs\/([^/]+)\/(.*)\.json$/,
  modules,
);

async function loadLocaleMessages(lang: SupportedLanguagesType) {
  if (unref(i18n.global.locale) === lang) {
    return setI18nLanguage(lang);
  }
  setSimpleLocale(lang);
  const message = await localesMap[lang]?.();
  if (message?.default) {
    i18n.global.setLocaleMessage(lang, message.default);
  }
  const mergeMessage = await loadMessages(lang);
  i18n.global.mergeLocaleMessage(lang, mergeMessage);
  return setI18nLanguage(lang);
}
```

## Conventions

- **Lazy chunks** — every `*.json` becomes a separate Vite chunk via
  `import.meta.glob`.
- **Idempotent loads** — calling `loadLocaleMessages(lang)` with the active
  lang is a no-op.
- **Type-safe locale union** — `'en-US' | 'zh-CN'` is closed; adding a
  locale requires a new entry in `langs/`.
- **Missing-key warning** is opt-in via `missingWarn: true`.
- **No `as any`** in this package — strict mode is enforced.
- **Tree-shake the public barrel** — `index.ts` only re-exports.

## Naming

| Thing | Convention | Example |
|---|---|---|
| JSON file | `kebab-case.json` | `authentication.json` |
| Locale code | `lang-REGION` | `en-US`, `zh-CN` |
| Key | `camelCase` | `loginSuccess` |
| Type | `PascalCase` | `LocaleSetupOptions` |

## Linting & pre-commit

- ESLint flat config (root)
- OxLint
- OxFmt (auto-format)
- Stylelint (does not apply here but kept consistent)
- `pnpm typecheck` includes `@vben/locales`

## Forbidden

- ❌ 不要 `import` 所有 locales at app entry — load lazily
- ❌ 不要 mutate `i18n.global.locale.value` directly — use `loadLocaleMessages`
- ❌ 不要 ship node_modules in `dist/` — keep build output clean
- ❌ 不要 add inline strings in `i18n.ts` — JSON files only
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 return `string` from `loadMessages` — `Promise<Record<string,string>>`
- ❌ 不要 use `i18n.global.t()` in JSON-bound code — types won't help
