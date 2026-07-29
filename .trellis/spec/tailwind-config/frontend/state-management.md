# @vben/tailwind-config: Theme Persistence

> This package declares **static** tokens. Theme **state** (light/dark) is managed by the **app** via `preferences` store.

## How theme state flows

```
┌──────────────────────────────────────────┐
│ App preferences (persisted: localStorage) │
│ preferences.theme.mode: 'auto'|'dark'|'light'
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ `usePreferences().setThemeMode(...)`     │
│ → root <html class="dark">               │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ `@custom-variant dark (&:is(.dark *))`  │
│ → tokens like `bg-bg-base-dark` apply     │
└──────────────────────────────────────────┘
                  ↓
┌──────────────────────────────────────────┐
│ Theme tokens from this package's `theme.css`│
└──────────────────────────────────────────┘
```

This package **owns** the tokens. The **app** owns theme mode state.

## Why theme.css doesn't read theme state

- It's a CSS file, not a Vue composable — it can't import from `@vben/preferences`
- Theme state → class on root → CSS selectors → token application. **No JS in the loop.**

## When to add a token

Add a token to `@theme inline` only if:
- ≥ 3 distinct Tailwind classes currently hard-code the same value
- It maps to a meaningful semantic concept ("primary", "warn", "error", not "blue")

## When to add a CSS variable fallback

If a CSS variable doesn't resolve (e.g., older browser), add a fallback in `theme.css`:

```css
--font-sans: var(--font-family), ui-sans-serif, system-ui, sans-serif;
```

## Forbidden

- ❌ Don't add `@media (prefers-color-scheme: dark)` queries to components — use `.dark` class via `@custom-variant`.
- ❌ Don't add JS to `theme.css` — keep it pure CSS.
- ❌ Don't store theme preference in localStorage from this package — apps do that.
- ❌ Don't read `preferences.theme.mode` from a token file.
