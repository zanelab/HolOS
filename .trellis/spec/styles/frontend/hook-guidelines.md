# @vben/styles Hook Guidelines

> No Vue hooks. CSS is the only deliverable.

## Purpose

`@vben/styles` is a CSS-only package. There are no `useXxx` composables,
no Pinia integration, and no JS runtime. The "hooks" here are the
**CSS class names** that components compose to get consistent styling
across the framework flavor.

## How composition happens

```vue
<!-- apps/web-antdv-next/src/views/authentication/login.vue (real pattern) -->
<script setup lang="ts">
import { useForm } from '@vben/hooks';
</script>

<template>
  <Form
    class="form-valid-error"
    :rules="formRules"
    @finish="handleSubmit"
  >
    <FormItem name="username" :rules="[{ required: true }]">
      <Input v-model:value="username" />
    </FormItem>
  </Form>
</template>
```

The `form-valid-error` class is the "hook" — when added, the flavor's
CSS rules paint the field in error state. `-color-danger` / `n-border-error`
are the underlying CSS variables.

## When a flavor needs reactive state

State stays in `@vben/preferences` (theme mode) and `@vben/stores` (locale,
settings). This package does not introduce new state.

```ts
// apps/web-antdv-next/src/app.vue
import { usePreferences } from '@vben/preferences';
const { isDark } = usePreferences();
```

The CSS uses `prefers-color-scheme` or design tokens — no direct
subscriptions.

## Reset pattern

```css
/* src/ele/index.css — element-plus reset */
.el-card {
  --el-card-border-radius: var(--radius) !important;
}

.form-valid-error {
  .el-select .el-select__wrapper {
    box-shadow: 0 0 0 1px var(--el-color-danger) inset;
  }
  .el-input .el-input__wrapper {
    box-shadow: 0 0 0 1px var(--el-color-danger) inset;
  }
}
```

`!important` is reserved for overriding third-party **`var()` defaults**
where the cascade order is locked.

## Conventions

- **No `useXxx()` exports** — pure CSS.
- **CSS variables** are the contract — never hardcode colors.
- **Class composition** — `.form-valid-error` is the cross-framework hook.
- **No `<style>` blocks** in component code that target framework
  resets — defer to the flavor CSS.
- **`bem` mixin** is exposed via `@vben-core/design/bem` for global SCSS.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Class (lib-scoped) | `.<lib>-<element>` | `.ant-btn`, `.el-card` |
| Class (workspace hook) | `.<scope>` | `.form-valid-error` |
| SCSS mixin | `bem(<block>, <elem>)` | `bem('card', 'header')` |

## Forbidden

- ❌ 不要 add `useXxx()` composables here — pure CSS package
- ❌ 不要 import `@vben/styles` into another `@vben/*` package — circular
- ❌ 不要 write JS in CSS files — no `<script>` blocks
- ❌ 不要 toggle theme via JavaScript here — `@vben/preferences` handles it
- ❌ 不要 override Tailwind tokens here — owned by `@vben-core/design`
- ❌ 不要 write `var(--foo-1)` literals — define them in design tokens
- ❌ 不要 add `prefers-color-scheme` listeners in this package
