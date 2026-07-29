# Web-Holos State Management

> **Don't reach for Pinia on every problem.**

## Decision Tree

| Where the state lives | Use |
|---|---|
| One component, one render | `ref()` / `reactive()` |
| One component, multiple children | provide / inject |
| Cross-route but app-global | `preferences` store |
| Cross-route user data | Pinia store |
| Server cache | API request |
| Cross-iframe / cross-tab | localStorage (only `preferences` writes there) |

## Pinia stores used in web-holos

- `useAccessStore` — tokens, access routes, access flags
- `useAuthStore` — login / register / logout
- `useUserStore` — current user info (`userInfo`, `avatar`, `homePath`)

## Persistence

- **Only `preferences` is persisted** in localStorage under `vben-web-tdesign-5.7.0-dev-preferences`
- **No persistence** for auth tokens (controlled by backend-mock or future real backend)

## Forbidden

- ❌ Don't persist auth tokens in localStorage (XSS)
- ❌ Don't add new pinia stores without a clear cross-component consumer
- ❌ Don't mutate preferences outside the store API (`updatePreferences(...)`)
