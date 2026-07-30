# @vben/styles Directory Structure

> Real layout for `packages/styles/`. Source verified 2026-07-30.

## Purpose

`@vben/styles` is the per-UI-framework CSS bundle. Each sub-package
(`antd`, `antdv-next`, `ele`, `naive`) ships a tight `index.css` file that
overrides and normalises the third-party component library's defaults so
the rest of the workspace can rely on consistent spacing, theming, and form
error visuals. A `global/` directory holds cross-framework extras.

## 目录树 (verified from `packages/styles/`)

```
@vben/styles/                       # workspace: packages/styles/
├── package.json                    # name "@vben/styles" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
├── index.ts                        # 单行: import '@vben-core/design'
├── style-exports.d.ts              # CSS module 类型声明
└── src/
    ├── index.ts                    # re-export everything via @vben-core/design
    ├── style-exports.d.ts          # declare const stylesheet: string
    ├── antd/
    │   └── index.css               # ant-design-vue reset + .form-valid-error
    ├── antdv-next/
    │   └── index.css               # ant-design-vue-next reset + .form-valid-error
    ├── ele/
    │   └── index.css               # element-plus reset + .form-valid-error
    ├── naive/
    │   └── index.css               # naive-ui reset + .form-valid-error
    └── global/
        └── index.scss              # 跨框架工具样式 (bem helpers)
```

## Real source (verified)

```ts
// packages/styles/src/index.ts
import '@vben-core/design';
```

```ts
// packages/styles/src/style-exports.d.ts
declare const stylesheet: string;
export default stylesheet;
```

```scss
// packages/styles/src/global/index.scss
@use '@vben-core/design/bem' as *;
```

The package is essentially a CSS multiplexer — no JS beyond the `import`
side-effect.

## Conventions

- **`src/<flavor>/index.css`** — exactly one CSS file per UI framework.
- **Flavor names** match the workspace app folder: `antd`, `antdv-next`,
  `ele`, `naive`, plus `global`.
- **`src/global/index.scss`** — framework-agnostic helpers (margin, scroll,
  typography fine-tuning).
- **`index.ts`** delegates to `@vben-core/design` (the real source of
  design tokens).
- **`style-exports.d.ts`** declares a `default: string` for full module
  type-safety on `import`.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Flavor dir | `<framework>` | `antd`, `antdv-next`, `ele`, `naive` |
| Flavor CSS | `index.css` | `src/antd/index.css` |
| Global CSS | `index.scss` | `src/global/index.scss` |
| Type file | `style-exports.d.ts` | — |

## Forbidden

- ❌ 不要引 入 其他 framework-specific reset (e.g., antd reset inside `ele/`)
- ❌ 不要 import other apps' styles here — workspace-level only
- ❌ 不要 redefine Tailwind tokens — owned by `@vben-core/design`
- ❌ 不要 add JS logic in `.css` / `.scss` files
- ❌ 不要 ship a `.min.css` directly — bundler handles it
- ❌ 不要 import `@vben/styles` from within `@vben-core` — circular
