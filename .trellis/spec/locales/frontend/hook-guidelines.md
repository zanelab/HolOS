# @vben/locales Hook Guidelines

> Pure data + i18n factory. No Vue composables defined here.

## Purpose

`@vben/locales` does not expose `useXxx()` composables. Locale loading is
explicit via `setupI18n(app)` and `loadLocaleMessages(lang)`. Apps that need
reactive locale state use `useSimpleLocale` from `@vben-core/composables`
(consumer concern, not part of this package).

## How locale is wired (no hooks)

```ts
// packages/locales/src/i18n.ts (verified)
import { createI18n } from 'vue-i18n';
import { useSimpleLocale } from '@vben-core/composables';

const i18n = createI18n({
  globalInjection: true,
  legacy: false,
  locale: '',
  messages: {},
});

const { setSimpleLocale } = useSimpleLocale();
```

`useSimpleLocale` lives in `@vben-core/composables` because it is a reactive
app-level state, not a package-level concern. `@vben/locales` only owns the
i18n instance.

## Switching language at runtime

```ts
// apps/web-antdv-next/src/store/auth.ts (real pattern)
import { $t } from '#/locales';
import { loadLocaleMessages } from '@vben/locales';

async function switchLanguage(lang: 'en-US' | 'zh-CN') {
  await loadLocaleMessages(lang);
  // $t reacts because i18n.global.locale is reactive
}
```

## Real composable consumer (app side)

```ts
// apps/web-antdv-next/src/locales/index.ts (real)
import { useI18n } from 'vue-i18n';

export const useAppI18n = () => {
  const { t, locale, availableLocales } = useI18n();
  return {
    availableLocales,
    locale,
    t,
  };
};
```

## Conventions

- **No `useXxx()` exports** from `@vben/locales` — keep i18n factory pure.
- **`globalInjection: true`** means `$t` / `$i18n` are auto-available in
  templates without explicit `useI18n()`.
- **`legacy: false`** — only composition API form, no `this.$t()`.
- **`loadLocaleMessages` is idempotent** — re-calling with the same lang is
  a no-op (early `return setI18nLanguage`).
- **Document `<html lang>`** is kept in sync by `setI18nLanguage`.
- **Missing handler** is opt-in via `missingWarn: true` to suppress noisy
  warnings in production.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Locale setup fn | `setupI18n(app, options?)` | `setupI18n(app)` |
| Loader fn | `loadLocaleMessages(lang)` | `loadLocaleMessages('zh-CN')` |
| Hooks | none — defined in `@vben-core/composables` | — |

## Forbidden

- ❌ 不要 add `useLocale()` 在这个 package — already handled by Vue I18n
- ❌ 不要 define `ref()` / `reactive()` for locale state in i18n.ts
- ❌ 不要 directly mutate `i18n.global.locale` — use `loadLocaleMessages`
- ❌ 不要 create side-effects in `setupI18n` outside `app.use(i18n)`
- ❌ 不要 import `useSimpleLocale` from this package — it lives in composables
- ❌ 不要 subscribe to `i18n.global` with `watch()` in this package
