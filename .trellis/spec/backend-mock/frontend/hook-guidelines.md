# @vben/backend-mock: No Hooks

> Nitro Mock Server has no Vue hooks. Mock endpoints are HTTP handlers.

## 真实 Example

`apps/backend-mock/api/_app.ts` (Nitro 顶层 handler):

```ts
import { defineEventHandler } from 'h3';

export default defineEventHandler(async (event) => {
  // Middleware-like behavior — runs on every request
  console.log(`[${new Date().toISOString()}] ${event.method} ${event.path}`);
  return; // 继续到 next handler
});
```

但这不是 "hook" — 这是 middleware pattern,Nitro specific.

## Where to Define Mock Endpoints

- **单 endpoint**: `api/<resource>/<action>.<method>.ts`
- **Batched resources**: `api/<group>/<action>.ts`
- **Health check**: `api/status.ts` (root endpoint)

## Naming Convention in Detail

| Filename | URL |
|---|---|
| `login.post.ts` | POST /api/login |
| `codes.get.ts` | GET /api/codes |
| `[id].ts` | GET /api/:id |
| `user/[id].get.ts` | GET /api/user/:id |

## Built-ins (Nitro-specific, not Vue hooks)

| Concern | What to use |
|---|---|
| Pre-handler | `middleware/` directory + `defineEventHandler` |
| Shared types | `api/types.ts` + import |
| Error handler | `error.ts` at root + `createError` |

## Forbidden

- ❌ 不要 add Vue / React / Pinia 到 `@vben/backend-mock`
- ❌ 不要 add `useXxx` composables
- ❌ 不要 add `/hooks/` dir (this isn't a Vue app)
- ❌ 不要 add `nuxt/`, `next/`, etc. — Nitro is the runtime
- ❌ 不要 add real DB persistence — purely mock
