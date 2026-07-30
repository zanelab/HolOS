# @vben/backend-mock "Component" Style — Event Handlers

> No Vue components. Every "component" is an h3 event handler.

## Purpose

`@vben/backend-mock` does not ship Vue SFCs. The concept of a
"component" here is an **event handler** — `default export` of a
`<name>.ts` file that Nitro mounts at the matching URL path. They are
typed, single-responsibility, and read from `mock-data` only.

## Real handler (verified)

```ts
// apps/backend-mock/api/test.get.ts
import { defineEventHandler } from 'h3';

export default defineEventHandler(() => 'Test get handler');
```

```ts
// apps/backend-mock/api/status.ts
import { eventHandler, getQuery, setResponseStatus } from 'h3';
import { useResponseError } from '~/utils/response';

export default eventHandler((event) => {
  const { status } = getQuery(event);
  setResponseStatus(event, Number(status));
  return useResponseError(`${status}`);
});
```

## Real handler with auth

```ts
// apps/backend-mock/api/user/info.ts
import { eventHandler } from 'h3';
import { verifyAccessToken } from '~/utils/jwt-utils';
import { unAuthorizedResponse, useResponseSuccess } from '~/utils/response';

export default eventHandler((event) => {
  const userinfo = verifyAccessToken(event);
  if (!userinfo) {
    return unAuthorizedResponse(event);
  }
  return useResponseSuccess(userinfo);
});
```

## Real handler with body and cookies

```ts
// apps/backend-mock/api/auth/login.post.ts
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
  const findUser = MOCK_USERS.find(
    (item) => item.username === username && item.password === password,
  );
  if (!findUser) {
    return forbiddenResponse(event, 'Username or password is incorrect.');
  }
  const accessToken = generateAccessToken(findUser);
  const refreshToken = generateRefreshToken(findUser);
  setRefreshTokenCookie(event, refreshToken);
  return useResponseSuccess({ ...findUser, accessToken });
});
```

## Conventions

- **Single default export** — `defineEventHandler` or `eventHandler`.
- **Sync handlers** return a value; **async handlers** return `Promise<T>`.
- **Use `useResponseSuccess` / `useResponseError`** for the uniform
  `{ code, data, error, message }` envelope.
- **Use `verifyAccessToken(event)`** to gate authenticated endpoints.
- **Mutating endpoints** under `/api/system/*` are blocked by
  `middleware/1.api.ts` in demo mode.
- **No `console.log` in handlers** — Nitro logger handles it.

## Uniform response shape

```ts
// utils/response.ts (verified)
export function useResponseSuccess<T = any>(data: T) {
  return { code: 0, data, error: null, message: 'ok' };
}
export function useResponseError(message: string, error: any = null) {
  return { code: -1, data: null, error, message };
}
export function forbiddenResponse(event, message = 'Forbidden Exception') {
  setResponseStatus(event, 403);
  return useResponseError(message, message);
}
export function unAuthorizedResponse(event) {
  setResponseStatus(event, 401);
  return useResponseError('Unauthorized Exception', 'Unauthorized Exception');
}
```

## Naming

| Thing | Convention | Example |
|---|---|---|
| Handler | `<name>.<method>.ts` | `login.post.ts` |
| Generic handler | `<name>.ts` | `info.ts`, `all.ts` |
| Status mapping | `useResponseError(`${status}`)` | sets status code |
| Auth gate | `verifyAccessToken(event)` | — |

## Forbidden

- ❌ 不要 write inline `return { code: 0, ... }` — use `useResponseSuccess`
- ❌ 不要 change response envelope shape — apps depend on it
- ❌ 不要 call `setResponseStatus` after writing body — use `setResponseStatus` first
- ❌ 不要 import from `@vben/*` packages here — separate runtime
- ❌ 不要 reference internal addresses — treat `MOCK_USERS` as immutable
- ❌ 不要 add `console.log` — Nitro logger handles it
- ❌ 不要 add `~` aliases that bypass `tsconfig.json` paths
