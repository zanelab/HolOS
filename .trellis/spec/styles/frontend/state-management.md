# @vben/styles State Management

> Stateless. CSS is purely passive.

## Purpose

`@vben/styles` has no JS state. All "state" is the CSS cascade — class
names, custom properties, and media queries. The package does not own any
runtime variable; theme state is owned by `@vben/preferences` and design
tokens by `@vben-core/design`.

## Where reactive state lives

```ts
// apps/web-antdv-next/src/app.vue (real)
import { preferences, usePreferences } from '@vben/preferences';

const { isDark } = usePreferences();
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

The CSS bundle is static; the variables it reacts to are owned by
`@vben/preferences` (the `theme.mode` field) and `@vben-core/design`
(tokens).

## CSS variable surface

```css
/* Implicit contract surfaced by the package */
:root {
  --radius: 0.5rem;
  --primary: hsl(212 100% 45%);
  --ant-color-primary: var(--primary);
  --el-color-primary: var(--primary);
}
```

```ts
// packages/styles/src/index.ts
import '@vben-core/design';
```

The actual token definitions live in `@vben-core/design`. This package only
**re-applies** them per framework.

## State surface map

| Surface | Type | Owned by |
|---|---|---|
| Theme tokens | CSS variables | `@vben-core/design` |
| Theme mode | `Ref<'dark' | 'light'>` | `@vben/preferences` |
| Compact mode | boolean | `@vben/preferences` |
| Locale | `Ref<Locale>` | `@vben/locales` |
| Reset CSS | static | `@vben/styles/<flavor>` |

## Conventions

- **No `ref`/`reactive` in this package** — CSS-only.
- **Tokens read via CSS variables** — never via JS imports.
- **One flavor per app** — bundles stay small.
- **No runtime theme computation** — `@vben/preferences` handles it.
- **No Pinia store** for CSS state — designer-side concern.

## Forbidden

- ❌ 不要 create a Pinia store for theme state — `@vben/preferences` owns it
- ❌ 不要 import design tokens in this package — `@vben-core/design` owns them
- ❌ 不要 write `localStorage.setItem('theme', ...)` here
- ❌ 不要 bind CSS classes via reactive inline styles — static classes
- ❌ 不要 put `@media (prefers-color-scheme: dark)` rules in this package
   (preference is the source of truth)
- ❌ 不要 centralize all colors into one file — each flavor owns its overrides
- ❌ 不要 add computed state for cascade content
