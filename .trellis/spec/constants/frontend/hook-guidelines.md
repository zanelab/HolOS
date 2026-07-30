# @vben/constants: No Vue Hooks

> @vben/constants 是纯数据包 — 不含 Vue 响应式 / hooks.

## Where Vue reactivity 来了

App composables wrap constants:

```ts
// apps/web-holos/src/composables/use-current-layout.ts
import { computed } from 'vue';
import { usePreferences } from '@vben/preferences';
import type { LayoutType } from '@vben/constants';

export function useCurrentLayout() {
  const prefs = usePreferences();
  return computed<LayoutType>(() => prefs.app.layout);
}
```

## Built-ins (in the apps 包)

虽然 `@vben/constants` 本身无 hooks,vben monorepo apps 提供:

| Concern | Hook | Source |
|---|---|---|
| App config | usePreferences() | @vben/preferences |
| Layout type | useCurrentLayout() | apps 各自定义 (基于 @vben/constants + @vben/preferences) |
| User info | useUserStore() | @vben/stores |

## Why this package has no hooks

- Constants 是 **静态** — 同一份 code 在所有 app 都是相同 const 值
- Vue 响应式要求 reactive wrappers(为 subscribe changes)
- `usePreferences()` 包了 `prefs.app.layout` 让它 reactive — 那 not @vben/constants 自己的事
- 保持 @vben/constants **leaf-package** 不引入 Vue 依赖

## Forbidden

- ❌ 不要在 `@vben/constants` 中添加 `ref()` / `reactive()` / `computed()`
- ❌ 不要在 `@vben/constants` 中添加 Pinia store
- ❌ 不要让 app layer 假设 `@vben/constants` 有 reactivity — 它是 pure values
- ❌ 不要 import Vue / Pinia / vue-router 进 `@vben/constants/src/*`
