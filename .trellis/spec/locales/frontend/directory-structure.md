# @vben/locales Directory Structure

> Real layout for `packages/locales/`. Source verified 2026-07-30.

## Purpose

`@vben/locales` is the workspace's i18n source of truth. It owns the `vue-i18n`
instance, lazy message loader, locale type definitions, and per-language JSON
dictionaries shared by every web-* app. Apps wire it up via `setupI18n(app)`
during bootstrap; consumers at runtime use `useI18n()` or the exported `$t`
global.

## 目录树 (verified from `packages/locales/`)

```
@vben/locales/                      # workspace: packages/locales/
├── package.json                    # name "@vben/locales" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
└── src/
    ├── index.ts                    # 公开 barrel — re-exports i18n, $t, $te, helpers
    ├── i18n.ts                     # createI18n + setupI18n + loadLocaleMessages
    ├── typing.ts                   # SupportedLanguagesType, LocaleSetupOptions
    └── langs/
        ├── en-US/
        │   ├── authentication.json
        │   ├── common.json
        │   ├── preferences.json
        │   ├── profile.json
        │   └── ui.json
        └── zh-CN/
            ├── authentication.json
            ├── common.json
            ├── preferences.json
            ├── profile.json
            └── ui.json
```

## Conventions

- **Top-level keys per language**: `authentication`, `common`, `preferences`,
  `profile`, `ui` — each maps to its own JSON file (one namespace = one file).
- **Lazy loading** via `import.meta.glob('./langs/**/*.json')` — every JSON file
  is a separate dynamic chunk, never bundled into the main entry.
- **Document lang attribute** is synced by `setI18nLanguage` in `i18n.ts`.
- **No business logic** — locales package is pure dictionaries + i18n setup.
- **Type-safe supported set** via `SupportedLanguagesType = 'en-US' | 'zh-CN'`.
- **`fallbackLocale`** is `en-US`; **`defaultLocale`** is `zh-CN`.

## App-side bootstrap

```ts
// apps/web-antdv-next/src/bootstrap.ts (verified)
import { $t, setupI18n } from '#/locales';

async function bootstrap(namespace: string) {
  const app = createApp(App);
  // 国际化 i18n 配置
  await setupI18n(app);
  // ...
  app.mount('#app');
}
```

## Naming

| Thing | Convention | Example |
|---|---|---|
| Locale code | `<lang>-<region>` | `en-US`, `zh-CN` |
| File key | kebab/single-word | `authentication.json` |
| Translation key | `namespace.path.to.value` | `authentication.loginSuccess` |
| Public helper | `$t` / `$te` / `i18n` / `useI18n` | — |

## Forbidden

- ❌ 不要在 Vue 组件内写硬编码字符串 (`'Login'`) — use `$t()`
- ❌ 不要 place 业务 logic in `i18n.ts` — only setup + loaders
- ❌ 不要 import 所有 `import * from './langs/...'` — use `import.meta.glob`
- ❌ 不要把 translations 放 `src/some-translation.ts` — JSON only
- ❌ 不要修改 `SupportedLanguagesType` 不修改 `langs/`
- ❌ 不要在 app 端 re-create `createI18n()` — use `setupI18n` from this package
