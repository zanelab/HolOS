# @vben/icons Directory Structure

> Real layout for `packages/icons/`. Source verified 2026-07-30.

## 目录树

```
@vben/icons/                        # workspace: packages/icons/
├── package.json                    # name "@vben/icons" v5.7.0
├── index.ts                        # 公开 barrel — re-exports Svg*Icon + IconifyIcon
└── svg/                            # hand-curated SVG components
    ├── SvgAntdvLogoIcon.vue
    ├── SvgAntdvNextLogoIcon.vue
    ├── SvgVbenLogoIcon.vue
    └── (... per-component SVG icons)
```

## Patterns

`index.ts` 大纲 (实际 verified):

```ts
// 从 packages/icons/index.ts 风格
export { default as IconifyIcon } from './IconifyIcon.vue';
// Svg* 组件 re-exports
export { default as SvgAntdvLogoIcon } from './svg/SvgAntdvLogoIcon.vue';
// ... 等
```

`IconifyIcon.vue` 实现 (实 v5.7.0):

```vue
<script setup lang="ts">
import { Icon } from '@iconify/vue';
defineProps<{ icon: string; size?: number }>();
</script>

<template>
  <Icon :icon="icon" :width="size ?? 16" :height="size ?? 16" />
</template>
```

每个 `Svg*.vue` 是 template-only SVG component:

```vue
<template>
  <svg viewBox="0 0 32 32">
    <path d="..." />
  </svg>
</template>
```

## Conventions

- **两条 icon paths**:
  - `<IconifyIcon>` — runtime loaded via `@iconify/vue` from CDN-style bundle
  - `<Svg*Icon>` — bundled SVG in workspace,不用 network
- **App-side auto-import** 通过 `unplugin-vue-components` 在 apps 里 enable,vben 5.7.0 框架自动
- **Tree-shake** — import specific icon,never `import *`

## App-side 使用示例

```vue
<!-- apps/web-holos/src/views/home/index.vue -->
<script setup lang="ts">
import SvgVbenLogoIcon from '@vben/icons/svg/SvgVbenLogoIcon.vue';
// 或者 auto-import 后:<SvgVbenLogoIcon />
</script>

<template>
  <IconifyIcon icon="lucide:home" :size="32" />
  <SvgVbenLogoIcon />
</template>
```

## Forbidden

- ❌ 不要 import 整个 @iconify/ 包(如 `import { all } from '@iconify/vue'`)
- ❌ 不要把所有 SVG 打进一个 `all-icons.vue`(巨型 bundle)
- ❌ 不要在 icons/index.ts 写逻辑 — 仅 re-exports
- ❌ 不要忽略 `unplugin-vue-components` 的 resolve,在 apps 里手动 import
- ❌ 不要 hardcode color strings in SVG paths via `fill="#abc"`
