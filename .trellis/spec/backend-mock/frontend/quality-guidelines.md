# @vben/backend-mock Quality Guidelines

> h3 handlers, uniform envelope, in-memory mocks.

## Purpose

`@vben/backend-mock` is the dev-time API surface. The quality bar is
"identical response shape every time, every endpoint goes through
`useResponseSuccess`/`useResponseError`, no DB, no surprise headers."

## TS file style

```ts
// apps/backend-mock/api/auth/login.post.ts (real)
import { defineEventHandler, readBody, setResponseStatus } from 'h3';
import { setRefreshTokenCookie } from '~/utils/cookie-utils';
import { generateAccessToken, generateRefreshToken } from '~/utils/jwt-utils';
import { MOCK_USERS } from '~/utils/mock-data';
import { forbiddenResponse, useResponseError, useResponseSuccess } from '~/utils/response';

export default defineEventHandler(async (event) => {
  const { password, username } = await readBody(event);
  if (!password || !username) {
    setResponseStatus(event, 400);
    return useResponseError('BadRequestException', 'Username and password are required');
  }
  // ...
});
```

- **2-space indent**
- **Single quotes**
- **No semicolons**
- **Trailing newline**
- **`import type`** for type-only imports
- **`default export`** of a single handler

## Real handler types

```ts
// apps/backend-mock/api/user/info.ts
import { eventHandler } from 'h3';
import { verifyAccessToken } from '~/utils/jwt-utils';
import { unAuthorizedResponse, useResponseSuccess } from '~/utils/response';

export default eventHandler((event) => {
  const userinfo = verifyAccessToken(event);
  if (!userinfo) return unAuthorizedResponse(event);
  return useResponseSuccess(userinfo);
});
```

## Conventions

- **Handlers are short** — under ~50 lines each.
- **Use `defineEventHandler` or `eventHandler`** — same convention.
- **Uniform response envelope** — `{ code, data, error, message }`.
- **All authenticated handlers** gate via `verifyAccessToken(event)`.
- **No `console.log`** — Nitro logger handles it.
- **No DB** — pure in-memory `MOCK_*` constants.
- **No `~` aliases beyond `tsconfig.json`** — properly configured paths.

## Strict mode

```ts
// apps/backend-mock/utils/response.ts
import type { EventHandlerRequest, H3Event } from 'h3';
import { setResponseStatus } from 'h3';

export function useResponseSuccess<T = any>(data: T) {
  return { code: 0, data, error: null, message: 'ok' };
}
```

`<T = any>` is allowed in response helpers — the data shape is
implicit. State and JWT utilities use specific types.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Handler | `<name>.<method>.ts` | `login.post.ts`, `test.get.ts` |
| Generic handler | `<name>.ts` | `info.ts`, `all.ts` |
| Mock data | `MOCK_<DOMAIN>` | `MOCK_USERS`, `MOCK_MENUS` |
| Envelope | `useResponseSuccess` / `useResponseError` | — |
| Status helper | `forbiddenResponse` / `unAuthorizedResponse` | — |

## Linting & pre-commit

- ESLint flat config
- OxLint
- OxFmt
- `pnpm typecheck` for backend-mock
- `pnpm dev:backend-mock` smoke test before commit

## Forbidden

- ❌ 不要 change response envelope shape — apps depend on it
- ❌ 不要 add `console.log` — Nitro logger handles it
- ❌ 不要 add Express — Nitro + h3 only
- ❌ 不要 mutate `MOCK_USERS` at runtime — treat as immutable
- ❌ 不要 bypass `verifyAccessToken` — uniform auth contract
- ❌ 不要 add `await` for sync handlers — sync where possible
- ❌ 不要 use `any` for handler inputs — type via `readBody<T>()` etc.
- ❌ 不要 skip `setResponseStatus` before `useResponseError`
