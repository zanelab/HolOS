# @vben/tailwind-config Type Safety

> 本包 **pure CSS**, no TS code beyond the 1-line `index.ts` re-export.

## 配置

`tsconfig.json` extends `@vben/tsconfig/library.json`:

```json
{
  "extends": "@vben/tsconfig/library.json"
}
```

But the only `.ts` file is `index.ts`:

```ts
// src/index.ts
import './theme.css';
```

That's it.

## 原因 no TypeScript matters for CSS

- Design tokens are **CSS custom properties** — types live at the value level, not the source level.
- **IntelliSense** for tokens comes from editor CSS plugins (e.g., Tailwind IntelliSense VS Code plugin).
- **Types** of token values are inferred from CSS, not declared.

## Tailwind v4 Type Safety Approach

- Tailwind v4 generates TypeScript types for utilities if you have `@types/node` installed.
- This project relies on **Tailwind IntelliSense** (VS Code plugin) for utility class validation.
- Color tokens that don't resolve go **silent in production** — make sure to test in dev.

## 禁止

- ❌ Don't add TS code to 本包 — keep it CSS-only.
- ❌ Don't import `@vben/preferences` or any other runtime dependency in `index.ts`.
- ❌ Don't add a `.ts` companion for design tokens — they're CSS variables.
- ❌ Don't import `index.ts` from Vue / TS code — apps should consume the CSS through Vite.

## Linting CSS in 本包

Stylelint runs on `theme.css` via the shared `internal/stylelint-config`.

Common checks enabled:
- `at-rule-no-unknown` — disables `@apply` etc. when not used
- `declaration-property-value-allowed-list` — restricts known-ok values
- `custom-property-pattern` — ensure `--token-name` consistent kebab-case

If you add a new lint rule, **declare it in `internal/stylelint-config/index.ts`**, not here.
