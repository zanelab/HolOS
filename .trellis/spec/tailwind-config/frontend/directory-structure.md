# @vben/tailwind-config Directory Structure

> Real layout for `internal/tailwind-config/` (workspace name `@vben/tailwind-config`).

## Tree (verified 2026-07-29)

```
internal/tailwind-config/
├── package.json              # name "@vben/tailwind-config" v5.7.0
├── tsconfig.json
└── src/
    ├── index.ts              # entry: import './theme.css' (re-exports the CSS as default)
    └── theme.css             # Tailwind v4 config — @theme tokens + scan globs + dark variant
```

## Conventions

- **Tailwind v4** style: design tokens live in `@theme { --font: ...; --color: ...; }` blocks inside `theme.css`. No `tailwind.config.ts` / `tailwind.config.js`.
- **Scan glob** discovers utility classes by scanning all packages:
  ```css
  @source '../../../packages/';
  @source '../../../apps/';
  @source '../../../docs/';
  @source '../../../playground/';
  ```
  When you add a new monorepo root, **add it here**.
- **Dark mode** uses `.dark` class variant (`@custom-variant dark`). Don't use `prefers-color-scheme` — this app supports manual theme switching.
- **Plugins** (`@tailwindcss/typography`, `@iconify/tailwind4`) are added via `@plugin` directives — no JS config.
- **Imports of this package** happen via `'@vben/tailwind-config/theme.css'` for old CSS imports, or the CSS is injected via Vite plugin. Apps don't directly consume `index.ts`.

## Forbidden

- ❌ Don't create `tailwind.config.ts` / `tailwind.config.js` — Tailwind v4 has moved entirely to CSS.
- ❌ Don't add new tokens to a separate `tokens.json` / `tokens.ts` — they go in `theme.css`'s `@theme { ... }` block.
- ❌ Don't import this package's `index.ts` directly from Vue/TS code — apps import the CSS via Vite.
- ❌ Don't add a build step for `theme.css` — it's already a plain CSS file consumed as-is.
