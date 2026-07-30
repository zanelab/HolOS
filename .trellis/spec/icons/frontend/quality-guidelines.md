# @vben/icons Quality Guidelines

> SVG + Iconify, tree-shake critical.

## SVG / Vue 风格

### SVG files (`*.vue` in svg/)

```vue
<template>
  <svg
    viewBox="0 0 24 24"
    xmlns="http://www.w3.org/2000/svg"
    role="img"
    aria-labelledby="title"
  >
    <title id="title">描述图标名称</title>
    <path d="..." fill="currentColor" />
  </svg>
</template>
```

- **2-space indent** for SVG 内部
- `<title>` for accessibility (读屏)
- `role="img"` for assistive tech
- `fill="currentColor"` to inherit CSS color
- ViewBox normalized to 24x24 或 32x32

### Vue SFC files

- **4-space** indent for `<script setup>`
- **Single quotes**
- **No semicolons**
- **Trailing newline**

## Naming

| Thing | Convention |
|---|---|
| SVG component | `Svg<Name>Icon.vue` (PascalCase) |
| Iconify name | `<family>:<name>` (kebab-case) |
| Wrapper component | `IconifyIcon.vue` (single global) |

## Tree-shaking

```ts
// ✅ Good — single SVG
import { SvgVbenLogoIcon } from '@vben/icons/svg/SvgVbenLogoIcon.vue';

// ❌ Bad — 全部 bundled icons
import { all } from '@vben/icons/all';
```

`icons/index.ts` **仅 re-export**,不引入所有 icon 全集。

## Pre-commit Hooks

- OxLint
- OxFmt (auto-format)
- ESLint flat config
- commitlint (`feat():` etc.)
- Stylelint (applies to SVG's inline `<style>` blocks)

## Code Style

```vue
<script setup lang="ts">
import type { PropType } from 'vue';

defineProps({
  icon: { type: String, required: true },
  size: { type: Number, default: 16 },
});
</script>

<template>
  <Icon
    :icon="icon"
    :width="size"
    :height="size"
  />
</template>
```

## Forbidden

- ❌ 不要 bundle 整个 Iconify icon collection (size 爆)
- ❌ 不要 inline `<svg>` in app components — 用 SvgXxxIcon
- ❌ 不要 hard-code colors (`fill="#ff0000"`) — use `currentColor` + CSS class
- ❌ 不要 skip `<title>` accessibility — 每 SVG 都有 title
- ❌ 不要在 app bundle 中所有 SVG-icons 一起打包 — tree-shake
- ❌ 不要 import `react-icons` / `vue-icons-vue` — use this package
