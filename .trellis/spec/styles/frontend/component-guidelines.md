# @vben/styles Component Guidelines

> No Vue components in this package. Only CSS bundles.

## Purpose

`@vben/styles` contains no JS components. The "components" here are
**CSS class hooks** — every CSS rule is a styling contract that web-*
components consume. Apps select the right flavor and import its CSS once
at bootstrap.

## How apps pick a flavor

```ts
// apps/web-antdv-next/src/bootstrap.ts (real)
import '@vben/styles';
import '@vben/styles/antdv-next';
```

```ts
// apps/web-ele/src/bootstrap.ts (real, similar pattern)
import '@vben/styles';
import '@vben/styles/ele';
```

`@vben/styles` (default = core tokens) is always imported first; the
flavor-specific CSS file is imported second to layer overrides.

## CSS class contracts

The CSS in this package exposes **named classes** that web-* views and
layout components rely on:

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
```

```css
/* packages/styles/src/naive/index.css */
.form-valid-error {
  .n-radio__dot {
    --n-box-shadow: inset 0 0 0 1px rgb(255 56 96);
  }
  .n-checkbox-box__border {
    --n-border: 1px solid rgb(255 56 96);
  }
}
```

Apps opt into the error visuals by wrapping the form:

```vue
<template>
  <Form class="form-valid-error">
    <FormItem name="email" :rules="emailRule">
      <NInput v-model:value="email" />
    </FormItem>
  </Form>
</template>
```

## Form-valid-error class

This is the workspace's cross-framework hook for marking a form whose
fields are in error state. The CSS rules vary per flavor (antd / ele /
naive) but the class name is identical, so layout components stay
framework-agnostic.

## Conventions

- **Class names are scoped per framework** — `.ant-x`, `.el-x`, `.n-x`.
- **`.form-valid-error`** is the workspace-level cross-framework hook.
- **No hardcoded colors** — use CSS custom properties (`--el-color-danger`,
  `--n-border-error`).
- **No `!important` outside the rare case of overriding third-party `var`**
  — plain cascade first.
- **Reset file** lives in `src/<flavor>/index.css` with explicit
  per-selector rules.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Selector | lib prefix + element | `.ant-btn`, `.el-card`, `.n-input` |
| Cross-framework hook | `.form-valid-error` | — |
| Global helper | BEM via `@vben-core/design/bem` | — |

## Forbidden

- ❌ 不要 override the third-party class names — use a wrapper class
- ❌ 不要 mix two flavors in one app — pick one
- ❌ 不要 use `!important` outside the rare `var` override
- ❌ 不要 import a flavor stylesheet you don't need — bundle bloat
- ❌ 不要 hardcode hex colors — use `var(--xxx)` or design tokens
- ❌ 不要 ship partial CSS files — `index.css` per flavor only
- ❌ 不要 write SCSS inside a `.css` file — tools will not run it
