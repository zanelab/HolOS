# @vben/locales State Management

> i18n state is owned by `vue-i18n` itself. This package does not hold extra state.

## Purpose

`@vben/locales` is stateless. The single reactive surface is `i18n.global`
(`locale`, `messages`, `availableLocales`). Mutations happen through the
controlled loader functions, not direct mutation.

## Reactive surfaces

```ts
// packages/locales/src/i18n.ts (real)
const i18n = createI18n({
  globalInjection: true,
  legacy: false,
  locale: '',
  messages: {},
});

// The reactive bits:
i18n.global.locale.value = 'en-US';              // current locale
i18n.global.setLocaleMessage('en-US', { ... }); // merge messages
i18n.global.setMissingHandler((locale, key) => {}); // missing key
i18n.global.mergeLocaleMessage('en-US', extra); // dynamic additions
```

`i18n.global.locale` is a `Ref<Locale>` — components that read it auto-rerender.
No Vue `ref` / `reactive` / `store` is defined inside this package.

## Extension: app-level locale state

If an app wants locale state outside the i18n context (e.g., to show a
language picker badge), it uses `useSimpleLocale` from `@vben-core/composables`:

```ts
// apps/web-antdv-next/src/locales/index.ts (real)
import { useSimpleLocale } from '@vben-core/composables';
const { setSimpleLocale, getSimpleLocale } = useSimpleLocale();
```

This is **app state**, not `@vben/locales` state.

## Message merging pattern

```ts
// i18n.ts setupI18n (real)
async function setupI18n(app: App, options: LocaleSetupOptions = {}) {
  const { defaultLocale = 'zh-CN' } = options;
  loadMessages = options.loadMessages || (async () => ({}));
  app.use(i18n);
  await loadLocaleMessages(defaultLocale);
  // 在控制台打印警告
  i18n.global.setMissingHandler((locale, key) => {
    if (options.missingWarn && key.includes('.')) {
      console.warn(
        `[intlify] Not found '${key}' key in '${locale}' locale messages.`,
      );
    }
  });
}
```

`loadMessages` lets apps inject extra runtime messages (e.g., per-route
overrides) without touching the core locale files.

## Conventions

- **Single source of truth** — only `i18n.global` is the reactive store.
- **No Pinia** in locales package.
- **No `ref` / `reactive`** for locale state — strictly delegation to vue-i18n.
- **Locale switching** is implemented via `loadLocaleMessages(lang)` only.
- **HTML `lang` attribute** is kept in sync by `setI18nLanguage`.

## State surface map

| Surface | Type | Where |
|---|---|---|
| `i18n.global.locale` | `Ref<Locale>` | mutable via `setI18nLanguage` |
| `i18n.global.messages` | `Record<Locale, Messages>` | mutable via `setLocaleMessage` |
| `i18n.global.availableLocales` | `Locale[]` | derived from messages |
| `i18n.global.missingHandler` | `(locale, key) => void` | set once in `setupI18n` |

## Forbidden

- ❌ 不要 create a Pinia store for locale state in this package
- ❌ 不要 persist `locale` to `localStorage` in this package — handled by app
- ❌ 不要 wrap `i18n.global` in a `reactive()` — it's already reactive
- ❌ 不要 bypass `loadLocaleMessages` and write directly to `setLocaleMessage`
  in app code (use the loader for caching/idempotency)
- ❌ 不要 hold translation strings in JS variables — JSON files only
- ❌ 不要建立 `currentLocale` ref in this package — use `i18n.global.locale`
