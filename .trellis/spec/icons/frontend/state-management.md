# @vben/icons: Stateless Icons

> Icons are pure-render. No reactivity in this package.

## 静态 Icons

```vue
<!-- SvgXxx 是纯 template,无 ref -->
<template>
  <svg viewBox="0 0 24 24"><path d="..." /></svg>
</template>
```

无 `ref`, `reactive`, 无 `defineStore`, 无 local state。

## IconifyIcon 是一种"动态名字的静态图标"

```vue
<!-- IconifyIcon 接受 icon prop, 但 icon 本身渲染 -->
<template>
  <Icon :icon="icon" />
</template>
```

无内部 reactive state — props change → 重新 render → 但 icons package 不持有 state。

## If You Need Reactive Icon

Apps wrap:

```ts
// apps/web-holos/src/composables/use-status-icon.ts
import { computed } from 'vue';

export function useStatusIcon(status: Ref<string>) {
  return computed(() => `lucide:${status.value}`);
}
```

The computed 里 `status.value` 改变时 icon 自动更新,但这是 **app concern**, not @vben/icons's。

## Forbidden

- ❌ 不要 export `ref()` / `reactive()` 在 icons package
- ❌ 不要添加 `useXxx()` composables 在 icons package
- ❌ 不要 wrap `<IconifyIcon>` 在 reactive containers — 包在 apps
- ❌ 不要 create Vuex store for icons (this codebase 用 Pinia)
- ❌ 不要用 `localStorage` 做 prefetched icons — that breaks SSR
