# Web-Holos 自定义 Hooks 规范

> 除非绝对必要，否则不要编写新的 hooks。

## 大部分动作映射到现有辅助函数

| Action | Use |
|---|---|
| Read/write app config | `usePreferences` from `@vben/preferences` |
| Call API | `requestClient.get/post` from `@vben/request` |
| Update user data | `useUserStore().setUserInfo(...)` |
| Login / logout | `useAuthStore()` methods |
| Permission check | `useAccessStore()` |

## 约定

- **One-line composable** rules: if `useFoo()` does not return reactive state or a stable function, **don't make it a hook** — make it a normal helper in `src/utils/`
- **Naming**: `useFoo` (camel case, starts with `use`)
- **文件位置**：
  - cross-module hooks → `src/hooks/`
  - page-scoped composables → co-located `useXxx.ts` next to the view

## 可用的内置函数（无需重新实现）

- `usePreferences` from `@vben/preferences` — read/write app config
- `useAccessStore` / `useUserStore` / `useAuthStore` from `@vben/stores`
- `useRouter` / `useRoute` from `vue-router`
- `useI18n` from `vue-i18n`
- `useDark`, `useScroll`, `useThrottleFn` from `@vueuse/core`

## 禁止

- ❌ Don't create wrapper hooks that just `return usePreferences()` — call `usePreferences()` directly
- ❌ 除非 **跨渲染保持状态**，不要在 hook 中放业务逻辑
- ❌ Don't use `watch` inside hooks without explicit `immediate: true`
