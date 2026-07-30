# @vben/backend-mock State Management

> In-memory `MOCK_*` constants. No DB. No Vue/Pinia.

## Purpose

`@vben/backend-mock` has **no persistent state**. The "state" is a set
of `MOCK_USERS`, `MOCK_MENUS`, `MOCK_TABLE`, and `MOCK_BIGINT`
constants in `utils/mock-data.ts`. They're reloaded on every Nitro
restart, making the dev experience predictable.

## State surface

```ts
// apps/backend-mock/utils/mock-data.ts (real, abridged)
export const MOCK_USERS: UserInfo[] = [
  { username: 'admin', password: 'admin123', roles: ['admin'], ... },
  { username: 'user', password: 'user123', roles: ['user'], ... },
  // ...
];

export const MOCK_MENUS = [
  { username: 'admin', menus: [ /* full menu tree */ ] },
  { username: 'user', menus: [ /* restricted menu tree */ ] },
];

export const MOCK_TABLE = [ /* 100 rows of demo data */ ];
```

```ts
// apps/backend-mock/utils/response.ts
export function useResponseSuccess<T = any>(data: T) {
  return { code: 0, data, error: null, message: 'ok' };
}
```

## Real handler reading state

```ts
// apps/backend-mock/api/menu/all.ts
import { verifyAccessToken } from '~/utils/jwt-utils';
import { MOCK_MENUS } from '~/utils/mock-data';

export default eventHandler(async (event) => {
  const userinfo = verifyAccessToken(event);
  if (!userinfo) return unAuthorizedResponse(event);
  const menus =
    MOCK_MENUS.find((item) => item.username === userinfo.username)?.menus ?? [];
  return useResponseSuccess(menus);
});
```

## State surface map

| Surface | Type | Owned by |
|---|---|---|
| `MOCK_USERS` | `UserInfo[]` | `utils/mock-data.ts` |
| `MOCK_MENUS` | `{ username, menus }[]` | `utils/mock-data.ts` |
| `MOCK_TABLE` | `TableRow[]` | `utils/mock-data.ts` |
| `MOCK_BIGINT` | `bigint[]` | `utils/mock-data.ts` |
| JWT secret | `string` | `utils/jwt-utils.ts` |
| Refresh token cookie | `httpOnly cookie` | `utils/cookie-utils.ts` |

## Conventions

- **No DB connection** — pure in-memory constant arrays.
- **Treat `MOCK_USERS` as immutable** — handlers `find` but don't mutate.
- **Mutations from `PUT/PATCH/POST/DELETE` to `/api/system/*`** are
  blocked by middleware in demo mode.
- **JWT-secret constants** are hardcoded in `jwt-utils.ts` (mock-only).
- **Cookie storage** is the only real persistence (`refreshToken`).
- **No Pinia** — it's a server runtime.

## Auth state machine

```ts
// Each endpoint gates:
const userinfo = verifyAccessToken(event);
if (!userinfo) return unAuthorizedResponse(event);
```

## Refresh token cookie

```ts
// utils/cookie-utils.ts
export function setRefreshTokenCookie(event: H3Event, token: string) {
  setCookie(event, 'refresh-token', token, {
    httpOnly: true,
    sameSite: 'none',
    secure: true,
    expires: /* 30 days */,
  });
}
```

## Naming

| Thing | Convention | Example |
|---|---|---|
| Mock data | `MOCK_<DOMAIN>` | `MOCK_USERS`, `MOCK_MENUS` |
| Handler state | read-only `MOCK_*` | `MOCK_USERS.find(...)` |
| Auth token | JWT in `Authorization: Bearer <token>` | — |
| Refresh token | `httpOnly` cookie | `refresh-token` cookie |

## Forbidden

- ❌ 不要 add a real database — in-memory `MOCK_*` only
- ❌ 不要 mutate `MOCK_USERS` at runtime — treat as immutable
- ❌ 不要 add SQLite / Postgres / anything — wrong layer
- ❌ 不要 add Pinia — server runtime
- ❌ 不要 bypass `verifyAccessToken` — uniform auth contract
- ❌ 不要 change JWT secret format — apps depend on it
- ❌ 不要 expose `MOCK_USERS.password` in plain responses — strip it
