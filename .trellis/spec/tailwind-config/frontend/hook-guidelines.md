# @vben/tailwind-config: Token-aware Patterns

> 本包 has no Vue hooks. Read this as "how apps should consume the tokens".

## 模式: prefer `theme.extend` over per-component tokens

When a Vue app needs a custom **local** color (e.g., "specific feature accent"), extend at the app's `src/index.css`, not in 本包:

```css
/* apps/web-holos/src/index.css */
@layer utilities {
  .holos-accent {
    color: oklch(0.69 0.21 142);
  }
}
```

Don't push one-off tokens upstream — keep 本包's tokens **global**.

## 模式: dark mode via `.dark` class

```vue
<script setup>
import { useDark } from '@vueuse/core';
const isDark = useDark({
  selector: 'html',
  attribute: 'class',
  valueDark: 'dark',
  valueLight: '',
});
</script>

<template>
  <div :class="isDark ? 'bg-bg-base-dark text-fg-primary-dark' : 'bg-bg-base text-fg-primary'">
    HolOS
  </div>
</template>
```

## 模式：响应式工具类

```html
<div class="flex flex-col md:flex-row gap-4 md:gap-8">
  <div class="w-full md:w-1/2">Column 1</div>
  <div class="w-full md:w-1/2">Column 2</div>
</div>
```

The `@source` directive in `theme.css` scans all packages + apps, so utility classes from any of them are preserved.

## 何时在代码中使用 本包 的 tokens

- **`bg-bg-base`** — page background, light mode white, dark mode `#0a0a0a`
- **`text-fg-primary`** — primary text
- **`border-border`** — default borders (light/dark variants)
- **`rounded-md` / `rounded-lg`** — corners referencing `--radius-*` tokens

## 禁止

- ❌ 不要在组件中硬编码 hex / rgb 颜色 — 使用语义化变量。
- ❌ Don't add `data-theme="dark"` style multi-theme logic — this app uses `.dark` class only.
- ❌ Don't add `tailwind.config.cjs` — Tailwind v4 doesn't use one.
- ❌ Don't bypass dark mode tokens by always using `bg-...` without `dark:` variant — Tailwind v4 will auto-pair dark tokens because of `@custom-variant dark`.
