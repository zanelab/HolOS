# @vben/backend-mock Type Safety

> Strict-mode TS for Nitro handlers.

## TS Config

`apps/backend-mock/tsconfig.json`:

```json
{
  "extends": "@vben/tsconfig/node.json"
}
```

Node config enables:
- `"strict": true`
- `"noUnusedLocals": true`
- `"target": "ES2022"` (Node 22+)

## Required Patterns

### 1. Define Event Handler with Type

```ts
// api/auth/login.post.ts
interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'Bearer';
  expires_in: number;
}

export default defineEventHandler(async (event): Promise<LoginResponse> => {
  const body = await readBody<LoginRequest>(event);
  // ...
  return { /* LoginResponse */ };
});
```

### 2. Type-safe ReadBody

```ts
// ✅ Generic param
const body = await readBody<LoginRequest>(event);

// ✅ Body parsing returns undefined for empty — narrow
if (!body) {
  throw createError({ statusCode: 400, message: 'Empty body' });
}
```

### 3. Error Helper

```ts
// createError from h3 — type-safe
throw createError({
  statusCode: 401,
  statusMessage: 'Unauthorized',
  message: 'Invalid credentials',
});

// ❌ Bad — throw plain Error
throw new Error('Unauthorized');  // 500 status
```

### 4. Type imports

```ts
import { defineEventHandler, readBody, createError, type EventHandlerRequest, type H3Event } from 'h3';
import type { NitroApp } from 'nitropack';
```

## Sharing Types

`api/types.ts` for cross-endpoint interfaces:

```ts
// api/types.ts
export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

export interface PaginatedList<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface User {
  id: string;
  username: string;
  realName: string;
  email?: string;
  avatar?: string;
  roles: string[];
}
```

## Forbidden

- ❌ 不要用 `any` — 用类型定义 in `types.ts`
- ❌ 不要 `throw new Error()` — 用 h3 `createError()` (返回 proper status)
- ❌ 不要用 `as` cast to silence errors — refactor
- ❌ 不要 return `Promise<any>` — 显式 generic
- ❌ 不要 disable strict mode per-file
- ❌ 不要 skip `@ts-ignore` / `@ts-expect-error` without `// why:` comment
- ❌ 不要用 Node legacy APIs (`require` 等) — strict ESM workspace
- ❌ 不要 export API routes that don't match `requestClient`'s types in app
