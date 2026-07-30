# @vben/backend-mock Type Safety

> h3 typed handlers, uniform response envelope, strict mode.

## Purpose

`@vben/backend-mock` is the strict-mode showcase for **Nitro + h3**.
Every handler is typed via `H3Event<EventHandlerRequest>`, the response
envelope is constant, and `import type` is mandatory.

## Handler typing

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
```

## Typed JWT payload

```ts
// apps/backend-mock/utils/jwt-utils.ts (verified)
import type { UserInfo } from './mock-data';

export interface UserPayload extends UserInfo {
  iat: number;
  exp: number;
}

export function generateAccessToken(user: UserInfo) {
  return jwt.sign(user, ACCESS_TOKEN_SECRET, { expiresIn: '7d' });
}

export function verifyAccessToken(
  event: H3Event<EventHandlerRequest>,
): null | Omit<UserInfo, 'password'> {
  // ...
}
```

## Typed body parsing

```ts
// apps/backend-mock/api/auth/login.post.ts
import { readBody, setResponseStatus } from 'h3';

interface LoginBody {
  username: string;
  password: string;
}

export default defineEventHandler(async (event) => {
  const body = await readBody<LoginBody>(event);
  const { password, username } = body;
  // ...
});
```

## Strict-mode patterns

### 1. Discriminated status

```ts
// ✅ Good — typed helper
export function setResponseStatus(event: H3Event, code: number): void;

// ❌ Bad — string code
setResponseStatus(event, '500' as any);
```

### 2. Typed handlers

```ts
// ✅ Good — explicit handler
import { defineEventHandler } from 'h3';
export default defineEventHandler((event) => 'OK');

// ❌ Bad — untyped event
export default (event: any) => 'OK';
```

### 3. Generic envelope

```ts
// ✅ Good — generic data
function useResponseSuccess<T = any>(data: T) {
  return { code: 0, data, error: null, message: 'ok' };
}

// ❌ Bad — bypass envelope
return { data: user }; // missing code/error/message
```

## TS config

```json
// apps/backend-mock/tsconfig.json
{
  "extends": "@vben/tsconfig/nitro.json",
  "compilerOptions": {
    "paths": {
      "~/*": ["./*"]
    }
  }
}
```

Strict mode + `verbatimModuleSyntax` + `noUnusedLocals`.

## Conventions

- **`import type`** for `H3Event`, `EventHandlerRequest`, `UserInfo`,
  `UserPayload`.
- **`defineEventHandler` / `eventHandler` typed** — `event` is typed.
- **Generic envelope** — `useResponseSuccess<T = any>(data: T)`.
- **No `as any` for handler inputs** — `readBody<T>()` typing.
- **Strict status code** — `setResponseStatus(event, 400)`, not `'400'`.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/backend-mock
```

## Forbidden

- ❌ 不要 use `any` for handler bodies — `readBody<T>()` instead
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 `as` casts to silence type errors — refactor
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 bypass `useResponseSuccess` / `useResponseError` — uniform envelope
- ❌ 不要 use untyped `event` params — explicit `H3Event<EventHandlerRequest>`
- ❌ 不要 expose `MOCK_USERS.password` in responses — strip via `Omit<>`
- ❌ 不要 `Promise<any>` for sync handlers — `T` directly
