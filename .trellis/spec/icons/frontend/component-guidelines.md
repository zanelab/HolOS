# @vben/icons "Component" Style — SVG + Iconify

> No Vue components in *this* package; components are SVG files + IconifyIcon wrapper.

## Pattern: IconifyIcon wrapper

```vue
<!-- icons/IconifyIcon.vue (real) -->
<script setup lang="ts">
import { Icon } from '@iconify/vue';
defineProps<{
  icon: string;       // 'lucide:home' / 'mdi:account' / ...
  size?: number;      // 默认 16
}>();
</script>

<template>
  <Icon :icon="icon" :width="size ?? 16" :height="size ?? 16" />
</template>
```

Usage:

```vue
<IconifyIcon icon="lucide:home" :size="24" />
```

## Pattern: SVG component

```vue
<!-- icons/svg/SvgVbenLogoIcon.vue -->
<template>
  <svg
    viewBox="0 0 32 32"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
  >
    <title>Vben Logo</title>
    <path d="M16 0L32 16L16 32L0 16Z" fill="currentColor" />
  </svg>
</template>
```

Important: `fill="currentColor"` 让 CSS `color:` 控制颜色。

## Tree-shake 验证

```ts
// ✅ Good — 只 import 用到的
import SvgVbenLogoIcon from '@vben/icons/svg/SvgVbenLogoIcon.vue';

// ❌ Bad — 全部引入
import * as Icons from '@vben/icons';
```

## Auto-import in apps

`apps/web-*/vite.config.ts` 应该:

```ts
import { defineConfig } from '@vben/vite-config';

export default defineConfig({
  plugins: [
    VbenComponents({
      dts: 'src/types/components.d.ts',
      // ...
    }),
  ],
});
```

Components auto-imports `<SvgVbenLogoIcon />`, `<IconifyIcon />` based on filename pattern.

## Naming

| Thing | Convention | Example |
|---|---|---|
| SVG component | `Svg<Name>Icon.vue` | `SvgVbenLogoIcon.vue` |
| Wrap component | `IconifyIcon.vue` | (single global component) |
| Iconify icon name | `<family>:<name>` | `lucide:home`, `mdi:account-circle` |

## Forbidden

- ❌ 不要 inline `<svg>` in app components — 用 SvgXxxIcon
- ❌ 不要混合 IconifyIcon + Svg*Icon 在同一个文件 — choose one
- ❌ 不要 import 从 `@iconify/vue` 顶层 — 用这个 wrapper 隔离
- ❌ 不要写 SVG 颜色改 hard-coded literals,use `currentColor` + CSS
- ❌ 不要在 SVG components 添加 ts script(unless 接收 props)
