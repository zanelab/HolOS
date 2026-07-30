# @vben/constants: Pure Data

> `packages/constants` 是 **静态数据** — 没有 reactivity / no caching.

## Implications

- 所有 const 在 module load 时 evaluate 一次
- 任何 reactivity 都属 app layer(@vben/preferences + composables)
- 安全 import 到任何 module(无 timing 依赖)

## Why this package stays stateless

- **Cross-app consistency** — 同一值在 web-holos / web-antd / web-tdesign 都相同
- **SSR-safe** — no global registry,no hydration concerns
- **Tree-shake** — bundler 知道 const values 不需要 runtime state

## Examples of cross-app 共享

| Constants | Used in |
|---|---|
| `LOGIN_PATH = '/auth/login'` | 所有 vben apps router/guard.ts |
| `HOME_PATH = '/dashboard'` | preferences default home path |
| `LAYOUT_TYPES` | preferences store validation schema |

## Forbidden

- ❌ 不要在 module-level 放 mutable vars
- ❌ 不要在 constants 加 `Symbol(...)` global registry
- ❌ 不要把 IO-fetched data 放在这里 — 那是 app concern via @vben/request
- ❌ 不要 export Vue Composition API 默认值 — 仅 plain values
