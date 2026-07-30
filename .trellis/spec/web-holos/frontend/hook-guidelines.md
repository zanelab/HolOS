# Web-Holos Custom Hooks Guidelines

> 除非绝对必要，否则不要写新 hooks.

## Most actions map to existing helpers

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
- **File location**:
  - cross-module hooks → `src/hooks/`
  - page-scoped composables → co-located `useXxx.ts` next to the view

## 可用的内置函数 (no need to re-implement)

- `usePreferences` from `@vben/preferences` — read/write app config
- `useAccessStore` / `useUserStore` / `useAuthStore` from `@vben/stores`
- `useRouter` / `useRoute` from `vue-router`
- `useI18n` from `vue-i18n`
- `useDark`, `useScroll`, `useThrottleFn` from `@vueuse/core`

## 禁止

- ❌ Don't create wrapper hooks that just `return usePreferences()` — call `usePreferences()` directly
- ❌ Don't put business logic in hooks unless **stateful across renders**
- ❌ Don't use `watch` inside hooks without explicit `immediate: true`
