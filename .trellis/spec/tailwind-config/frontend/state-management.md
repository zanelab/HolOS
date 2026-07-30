# @vben/tailwind-config: Theme Persistence

> 本包 declares **static** tokens. Theme **state** (light/dark) is managed by the **app** via `preferences` store.

## 主题状态如何流转

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

本包 **owns** the tokens. The **app** owns theme mode state.

## 原因 theme.css doesn't read theme state

- It's a CSS file, not a Vue composable — it can't import from `@vben/preferences`
- Theme state → class on root → CSS selectors → token application. **无 JS in the loop.**

## 何时添加一个 token

Add a token to `@theme inline` only if:
- 至少 3 个不同的 Tailwind 类当前硬编码同一值
- 对应有意义的语义概念（"主题"、"警示"、"错误"，而非 "蓝"）

## 何时 add a CSS variable fallback

If a CSS variable doesn't resolve (e.g., older browser), add a fallback in `theme.css`:

```css
--font-sans: var(--font-family), ui-sans-serif, system-ui, sans-serif;
```

## 禁止

- ❌ Don't add `@media (prefers-color-scheme: dark)` queries to components — use `.dark` class via `@custom-variant`.
- ❌ Don't add JS to `theme.css` — keep it pure CSS.
- ❌ Don't store theme preference in localStorage from 本包 — apps do that.
- ❌ Don't read `preferences.theme.mode` from a token file.
