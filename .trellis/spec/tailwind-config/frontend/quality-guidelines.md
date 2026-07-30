# @vben/tailwind-config Quality Guidelines

> Tailwind v4 — CSS-driven config, not JS.

## Code Style

- **2 spaces** indent for CSS (unlike TS which is 4)
- **Single quotes** for CSS strings (when used)
- **Sort `@source` globs alphabetically** by line — keeps diffs easy to read
- **Comment group headers** as `/* Group Name */` above each token block in `theme.css`

## 命名约定 Tokens

Use **semantic** names, not appearance:

| ✅ Use | ❌ Avoid |
|---|---|
| `--color-fg-primary` | `--color-blue-700` |
| `--color-bg-base` | `--color-gray-100` |
| `--spacing-md` | `--space-12px` |
| `--radius-md` | `--radius-6px` |
| `--font-sans` | `--font-roboto` |

Avoid `--color-bg-white` — when dark mode is enabled, `bg-bg-base` should automatically resolve to `bg-bg-base-dark` via the `.dark` selector.

## Adding Tokens

```css
/* Group Name */
@theme inline {
  --token-name: value;
  --token-another: value;
}
```

For **complex values** that need to compose:

```css
/* Border Radius */
--radius-sm: calc(var(--radius) - 4px);
```

## 禁止

- ❌ Don't add `tailwind.config.ts` / `tailwind.config.js` — Tailwind v4 doesn't use one. The config IS the CSS.
- ❌ Don't hard-code hex / `rgb()` directly in components — extend `theme.css`.
- ❌ Don't add `@media (prefers-color-scheme: dark)` to components — use `.dark` class via `@custom-variant dark`.
- ❌ Don't add new utility classes that bypass `@theme` — utilities should derive from tokens.
- ❌ Don't break the alphabetical sort of `@source` globs.

## Lint / Format

- **Stylelint** is shared via `internal/stylelint-config`. Run `pnpm lint:fix` to auto-fix.
- **Prettier** for final formatting (`internal/oxfmt-config`).
