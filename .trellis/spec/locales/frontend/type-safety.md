# @vben/locales Type Safety

> Locale union types are closed; `import type` enforced.

## Purpose

`@vben/locales` is the strict-mode showcase package. Every locale string,
every setup option, and every loader is fully typed. Adding a new language
is a compile-time-affecting change — `SupportedLanguagesType` must be edited
and the new directory created under `langs/`.

## Locale union

```ts
// packages/locales/src/typing.ts (verified)
export type SupportedLanguagesType = 'en-US' | 'zh-CN';

export type ImportLocaleFn = () => Promise<{ default: Record<string, string> }>;

export type LoadMessageFn = (
  lang: SupportedLanguagesType,
) => Promise<Record<string, string> | undefined>;

export interface LocaleSetupOptions {
  defaultLocale?: SupportedLanguagesType;
  loadMessages?: LoadMessageFn;
  missingWarn?: boolean;
}
```

## Public barrel re-exports

```ts
// packages/locales/src/index.ts
export {
  type ImportLocaleFn,
  type LocaleSetupOptions,
  type SupportedLanguagesType,
} from './typing';
export type { CompileError } from '@intlify/core-base';
export { useI18n } from 'vue-i18n';
export type { Locale } from 'vue-i18n';
```

All type-only exports use the `export { type X }` syntax (no `import type` in
re-export position).

## TS config

```json
// packages/locales/tsconfig.json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` enabled. `noUnusedLocals` and
`noUnusedParameters` are enforced.

## Real typed example: app bootstrap

```ts
// apps/web-antdv-next/src/bootstrap.ts
import { $t, setupI18n } from '#/locales';
import { useTitle } from '@vueuse/core';

async function bootstrap(namespace: string) {
  const app = createApp(App);
  // setupI18n is typed: (app: App, options?: LocaleSetupOptions) => Promise<void>
  await setupI18n(app);
  // ...
  watchEffect(() => {
    if (preferences.app.dynamicTitle) {
      const routeTitle = router.currentRoute.value.meta?.title;
      const pageTitle =
        (routeTitle ? `${$t(routeTitle)} - ` : '') + preferences.app.name;
      useTitle(pageTitle);
    }
  });
}
```

## Strict-mode patterns

### 1. Locale argument typing

```ts
// ✅ Good — typed by union
async function switchLang(lang: SupportedLanguagesType) {
  await loadLocaleMessages(lang);
}

// ❌ Bad — accepts any string
async function switchLang(lang: string) {
  await loadLocaleMessages(lang); // type error if not in union
}
```

### 2. Loader return type

```ts
// ✅ Good — explicit return
export type ImportLocaleFn = () => Promise<{ default: Record<string, string> }>;

// ❌ Bad — any leaks in
export type ImportLocaleFn = () => Promise<any>;
```

### 3. Setup options

```ts
// ✅ Good — interface with optional fields
const opts: LocaleSetupOptions = {
  defaultLocale: 'zh-CN',
  missingWarn: true,
};

// ❌ Bad — bypasses the union
const opts = {
  defaultLocale: 'fr-FR', // type error
};
```

## Conventions

- **Every exported type** lives in `typing.ts` and is re-exported from
  `index.ts` via `export { type X }`.
- **No `any`** in returns — `Promise<Record<string, string> | undefined>`.
- **`import type`** for type-only imports (e.g., `import type { App } from 'vue'`).
- **Closed unions** — extending `SupportedLanguagesType` requires touching
  both the type and `langs/`.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/locales
```

## Forbidden

- ❌ 不要 use `any` for locale strings — restrict to `string` or union
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 `as` casts to silence type errors — refactor
- ❌ 不要 use `@ts-ignore` without a `// why:` comment
- ❌ 不要 add `Record<string, any>` for messages — use `Record<string, string>`
- ❌ 不要 publish a `dist/` that is `verbatimModuleSyntax` rule-violating
- ❌ 不要 extend the language union without populating `langs/<lang>/`
