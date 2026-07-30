# @vben/web-naive State Management

> Pick the simplest container that fits. Don't reach for Pinia first.

## Decision Tree

| Where the state lives | Use |
|---|---|
| One component, one render | ref() / reactive() |
| One component, deep children | provide() / inject() |
| Cross-page, persisted | preferences store |
| Cross-page, transient | Pinia store (@vben/stores) |
| Server cache | API + useAsyncResource |

## Pinia 状态存储 (canonical 3)

- useAccessStore - tokens / access routes / flags
- useAuthStore - login / logout / token expiry
- useUserStore - current user, avatar, homePath

## App-Specific Pattern

`preferences.ts` may declare a typed preferences extension.
