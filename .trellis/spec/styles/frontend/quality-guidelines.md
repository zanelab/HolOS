# @vben/styles Quality Guidelines

> CSS-only package. Cascade-clean, token-driven, framework-isolated.

## Purpose

`@vben/styles` is the workspace's CSS contract. The quality bar is: every
class is scoped per framework, every color flows through a CSS variable,
no surprises when the bundle is purged.

## CSS file style

```css
/* packages/styles/src/antdv-next/index.css (real excerpt) */
.ant-app {
  width: 100%;
  height: 100%;
  overscroll-behavior: none;
  color: inherit;
}

.ant-btn {
  .anticon {
    display: inline-flex;
  }
  > svg {
    display: inline-block;
  }
  > svg + span {
    margin-inline-start: 6px;
  }
}

.ant-tag {
  > svg {
    display: inline-block;
  }
}
```

- **2-space indent**
- **No `!important`** outside the rare `var()` override
- **No shorthand hex** — `hsl()` preferred via design tokens
- **No `*` selectors** — explicit selectors only
- **No `@import` inside CSS** — bundler handles asset graph

## SCSS file style

```scss
/* packages/styles/src/global/index.scss */
@use '@vben-core/design/bem' as *;
```

- **2-space indent**
- **`@use` for module imports** (no `@import` per Sass 1.79+)
- **No magic numbers** — use design tokens

## Conventions

- **One CSS file per flavor** — never split mid-file.
- **`!important` only for `var()` overrides** — flagged with comment.
- **Selector specificity** — match the framework's class, then add
  workspace hooks below.
- **No `font-` rules** — typography is owned by the design tokens.
- **Pre-flavor reset** (`@vben/styles`) **before flavor-specific**
  (`@vben/styles/<flavor>`).
- **No global selectors** in flavor CSS — scope under the framework
  prefix.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Selector | `.<lib>-<element>` | `.ant-btn`, `.el-card` |
| Workspace hook | `.<scope>` | `.form-valid-error` |
| SCSS mixin | `bem(<block>, <elem>)` | `bem('card', 'header')` |
| CSS file | `index.css` per flavor | `src/ele/index.css` |

## Linting & pre-commit

- Stylelint (root config) — every CSS/SCSS file
- ESLint / OxLint for `.ts` files
- OxFmt (auto-format)
- `pnpm typecheck` for `style-exports.d.ts` validity

## Forbidden

- ❌ 不要 `!important` outside `var()` override — plain cascade first
- ❌ 不要 hardcode hex / `rgb()` literals — use design tokens
- ❌ 不要 `* { margin: 0 }` global reset — broken cascade
- ❌ 不要 `@import url(...)` inside CSS — bundler handles assets
- ❌ 不要 mixed element-plus + antd selectors in one file
- ❌ 不要 declare `:root` selectors in flavor CSS — global tokens only
- ❌ 不要 ship `.min.css` directly — bundler handles it
- ❌ 不要 write JS inside `.css` — no script blocks
