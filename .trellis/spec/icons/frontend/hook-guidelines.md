# @vben/icons: No Vue Hooks

> Icon components are render-only. No Vue hooks in this package.

## Why no hooks

- IconifyIcon 一次渲染,属性变化通过 props 传
- Svg*Icon 是 template-only, 没有 reactive state
- 应用层需要 reactive icon switching 时, 包成 composable

## 动态 Icon 切换 (in apps)

When user state affects icon:

```ts
// apps/web-holos/src/composables/use-theme-icon.ts
import { usePreferences } from '@vben/preferences';
import { computed } from 'vue';

export function useThemeIcon() {
  const prefs = usePreferences();
  return computed(() =>
    prefs.theme.mode === 'dark' ? 'lucide:moon' : 'lucide:sun'
  );
}
```

Usage in Vue:

```vue
<script setup>
import { IconifyIcon } from '@vben/icons';
import { useThemeIcon } from '#/composables/use-theme-icon';

const icon = useThemeIcon();
</script>

<template>
  <IconifyIcon :icon="icon" :size="20" />
</template>
```

## Built-ins (in apps, not in icons package)

| Icon 需要 reactive 选 | 用法 |
|---|---|
| Theme icon | computed() on `prefs.theme.mode` |
| User role icon | computed() on `userStore.roles` |
| Status icon | computed() on prop value |

## Forbidden

- ❌ 不要在 `@vben/icons` 中添加 `useXxx` hooks
- ❌ 不要让 icon 自动响应 user state — 那应该 app side computed
- ❌ 不要在 IconifyIcon.vue 添加 `onMounted` / `watch`
- ❌ 不要在 Svg*Icon.vue 创 ref / reactive
