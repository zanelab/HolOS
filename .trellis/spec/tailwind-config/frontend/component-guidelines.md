# @vben/tailwind-config "Component" Style — Design Tokens

> 本包 has **no Vue components**. Its "components" are **design tokens declared in CSS**.

## 模式: tokens as CSS custom properties

In `src/theme.css`:

```css
@theme inline {
  /* Border Radius (CSS variables reference) */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  /* Color tokens (dark / light variants) */
  --color-bg-base: #ffffff;
  --color-bg-base-dark: #0a0a0a;
  --color-fg-primary: #0f172a;
  --color-fg-primary-dark: #f1f5f9;
}
```

In app code (an app's `src/index.css`):

```css
/* Tailwind's safelist — these classes must NOT be tree-shaken */
.btn-primary {
  @apply px-4 py-2 rounded-md bg-blue-500 text-white;
}
```

The app consumes tokens **without redefining them** — Tailwind v4's `@theme inline` injects them into utility classes (`rounded-md` → `border-radius: var(--radius-md)`).

## 添加新的 Token

1. Add `/* Color */` group in `src/theme.css` under `@theme inline { ... }`
2. Add `bg-` / `text-` / `border-` classes in `theme.css`'s `@theme` if it's a new color slot
3. Test in `@vben/web-holos/src/index.css` (the dev target app)

## 添加新的插件

```css
@import 'tailwindcss';
@import 'tw-animate-css';

@plugin '@tailwindcss/typography';
@plugin '@iconify/tailwind4';
```

Plugins register themselves; no JS config required.

## 禁止

- ❌ Don't redefine tokens in app-level CSS — they belong in `theme.css` only.
- ❌ Don't hard-code colors (`bg-[#abc123]`) outside `theme.css` — use semantic tokens like `bg-primary`.
- ❌ Don't add new colors to a Tailwind preset (this is Tailwind v4 — no preset JS to modify).
- ❌ Don't override Tailwind classes with `!important` inside Vue components — extend `theme.css` instead.
