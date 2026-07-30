# Web-Holos 状态管理

> **Don't reach for Pinia on every problem.**

## 决策树

| 状态存放位置 | 用法 |
|---|---|
| One component, one render | `ref()` / `reactive()` |
| One component, multiple children | provide / inject |
| Cross-route but app-global | `preferences` store |
| Cross-route user data | Pinia store |
| Server cache | API request |
| Cross-iframe / cross-tab | localStorage (only `preferences` writes there) |

## web-holos 中使用的 Pinia stores

- `useAccessStore` — tokens, access routes, access flags
- `useAuthStore` — login / register / logout
- `useUserStore` — current user info (`userInfo`, `avatar`, `homePath`)

## 持久化

- **Only `preferences` is persisted** in localStorage under `vben-web-tdesign-5.7.0-dev-preferences`
- auth tokens **不持久化**（由 backend-mock 或未来真实 backend 控制）

## 禁止

- ❌ Don't persist auth tokens in localStorage (XSS)
- ❌ 没有明确的跨组件消费者不要新增 pinia store
- ❌ Don't mutate preferences outside the store API (`updatePreferences(...)`)
