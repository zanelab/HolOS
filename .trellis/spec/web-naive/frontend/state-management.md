# @vben/web-naive State Management

> 选择最合适的简单容器。不要一开始就上 Pinia。

## Decision Tree

| Where the state lives | Use |
|---|---|
| 单组件、一次渲染 | ref() / reactive() |
| 单组件、深度子组件 | provide() / inject() |
| 跨页面、需持久化 | preferences store |
| Cross-page, transient | Pinia store (@vben/stores) |
| Server cache | API + useAsyncResource |

## Pinia 状态存储（标准 3 个）

- useAccessStore - tokens / access routes / flags
- useAuthStore - login / logout / token expiry
- useUserStore - current user, avatar, homePath

## App-Specific Pattern

`preferences.ts` may declare a typed preferences extension.
