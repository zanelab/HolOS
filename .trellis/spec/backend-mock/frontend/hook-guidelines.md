# @vben/backend-mock Hook Guidelines

> No Vue hooks. Helper functions live in `utils/`.

## Purpose

`@vben/backend-mock` does not define `useXxx()` composables. The
"hooks" here are **utility functions** in `apps/backend-mock/utils/`
(`response.ts`, `jwt-utils.ts`, `cookie-utils.ts`, `mock-data.ts`,
`timezone-utils.ts`). Handlers in `api/` import these utilities
directly.

## Real utility: response envelope

```ts
// apps/backend-mock/utils/response.ts (verified)
import type { EventHandlerRequest, H3Event } from 'h3';
import { setResponseStatus } from 'h3';

export function useResponseSuccess<T = any>(data: T) {
  return { code: 0, data, error: null, message: 'ok' };
}

export function useResponseError(message: string, error: any = null) {
  return { code: -1, data: null, error, message };
}

export function forbiddenResponse(
  event: H3Event<EventHandlerRequest>,
  message = 'Forbidden Exception',
) {
  setResponseStatus(event, 403);
  return useResponseError(message, message);
}

export function unAuthorizedResponse(event: H3Event<EventHandlerRequest>) {
  setResponseStatus(event, 401);
  return useResponseError('Unauthorized Exception', 'Unauthorized Exception');
}

export function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function pagination<T = any>(
  pageNo: number,
  pageSize: number,
  array: T[],
): T[] {
  const offset = (pageNo - 1) * Number(pageSize);
  return offset + Number(pageSize) >= array.length
    ? array.slice(offset)
    : array.slice(offset, offset + Number(pageSize));
}
```

## Real utility: JWT

```ts
// apps/backend-mock/utils/jwt-utils.ts (verified)
import type { EventHandlerRequest, H3Event } from 'h3';
import { getHeader } from 'h3';
import jwt from 'jsonwebtoken';

import { MOCK_USERS } from './mock-data';

const ACCESS_TOKEN_SECRET = 'access_token_secret';
const REFRESH_TOKEN_SECRET = 'refresh_token_secret';

export function generateAccessToken(user: UserInfo) {
  return jwt.sign(user, ACCESS_TOKEN_SECRET, { expiresIn: '7d' });
}

export function verifyAccessToken(event: H3Event<EventHandlerRequest>) {
  const authHeader = getHeader(event, 'Authorization');
  if (!authHeader?.startsWith('Bearer')) return null;
  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, ACCESS_TOKEN_SECRET) as UserPayload;
    const user = MOCK_USERS.find((item) => item.username === decoded.username);
    return user ? { ...user, password: undefined } : null;
  } catch {
    return null;
  }
}
```

## How handlers use these helpers

```ts
// apps/backend-mock/api/auth/login.post.ts (real)
import { forbiddenResponse, useResponseError, useResponseSuccess } from '~/utils/response';
import { generateAccessToken, generateRefreshToken } from '~/utils/jwt-utils';
import { MOCK_USERS } from '~/utils/mock-data';

export default defineEventHandler(async (event) => {
  const { password, username } = await readBody(event);
  // ...
  const user = MOCK_USERS.find(...);
  if (!user) return forbiddenResponse(event, 'Username or password is incorrect.');
  return useResponseSuccess({
    ...user,
    accessToken: generateAccessToken(user),
  });
});
```

## Conventions

- **Helpers in `utils/`** — no `useXxx` Vue naming, only `useXxx` response helpers.
- **Pure functions** — `useResponseSuccess`, `pagination`, `sleep`.
- **Helpers take `event` as first arg** when they need to set status.
- **Typed by h3** — `H3Event<EventHandlerRequest>` for handler context.
- **No Pinia / Vue refs** in this package.
- **No `import type` from apps** — apps are runtime, not types.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Helper file | `<topic>-utils.ts` | `jwt-utils.ts`, `cookie-utils.ts` |
| Function | `verbXxx` | `useResponseSuccess`, `verifyAccessToken` |
| Status helper | `forbiddenResponse(event, msg)` | — |
| Pagination | `pagination(pageNo, pageSize, array)` | — |

## Forbidden

- ❌ 不要 write `useXxx()` Vue composables here — h3 handlers only
- ❌ 不要 import Vue runtime — Nitro is server runtime
- ❌ 不要 add Pinia stores — Nitro + h3 is the only state container
- ❌ 不要 bypass `useResponseSuccess` — uniform envelope
- ❌ 不要 take `event` as a context-less helper — pass it explicitly
- ❌ 不要 mutate `MOCK_USERS` / `MOCK_MENUS` — treat as immutable
- ❌ 不要 add `console.log` — Nitro logger handles it
