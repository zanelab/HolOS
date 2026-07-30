# @vben/backend-mock Component Guidelines

> Nitro Mock Server "Components" = HTTP endpoints.

## Pattern: defineEventHandler

```ts
// api/auth/login.post.ts (real)
import { defineEventHandler, readBody, createError } from 'h3';

interface LoginRequest {
  username: string;
  password: string;
}

export default defineEventHandler(async (event) => {
  const body = await readBody<LoginRequest>(event);

  if (!body.username || !body.password) {
    throw createError({
      statusCode: 400,
      message: 'Missing username or password',
    });
  }

  if (body.username !== 'vben' || body.password !== 'vben123') {
    throw createError({ statusCode: 401, message: 'Invalid credentials' });
  }

  return {
    access_token: 'mock-access-token',
    refresh_token: 'mock-refresh-token',
    expires_in: 3600,
  };
});
```

## Filename Convention

| Filename | HTTP Method | URL Pattern |
|---|---|---|
| `login.post.ts` | POST | /api/login |
| `codes.ts` (no .method) | GET | /api/codes |
| `[id].get.ts` | GET | /api/:id (dynamic param) |
| `logout.post.ts` | POST | /api/logout |

## Real Examples Used by Apps

```ts
// api/menu/all.ts — used by router/access.ts to fetch dynamic menus
export default defineEventHandler(() => {
  return [
    { id: 'dashboard', path: '/dashboard', title: '概览', icon: 'lucide:layout-dashboard' },
    { id: 'analytics', path: '/dashboard/analytics', title: '分析页' },
    // ...
  ];
});

// api/auth/refresh.post.ts — refresh JWT
export default defineEventHandler(async (event) => {
  const body = await readBody<{ refresh_token: string }>(event);
  if (!body.refresh_token) {
    throw createError({ statusCode: 400, message: 'Missing refresh_token' });
  }
  return {
    access_token: 'new-access-' + Date.now(),
    refresh_token: 'new-refresh-' + Date.now(),
    expires_in: 3600,
  };
});
```

## Type Patterns

```ts
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

// Use generics for type-safe body parsing
export default defineEventHandler(async (event): Promise<LoginResponse> => {
  const body = await readBody<LoginRequest>(event);
  // ...
});
```

## Error Handling

```ts
// ✅ Good
throw createError({
  statusCode: 401,
  message: 'Invalid credentials',
});

// ❌ Bad — returns 200 with error in body
return { success: false, error: '...' };
```

Nitro automatically maps `createError()` to proper HTTP response codes.

## Cross-cutting: shared types

`types.ts` at api/ root for shared interfaces:

```ts
// api/types.ts (建议)
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
```

## Forbidden

- ❌ 不要用 Express / Koa — 用 Nitro h3
- ❌ 不要 import client-side packages (Vue, React)
- ❌ 不要 mutations that break HTTP semantics
- ❌ 不要 forget `await readBody()` — 异步
- ❌ 不要 store sensitive data plain text in memory (mock only OK)
- ❌ 不要用 `console.log` for production diagnostics — Nitro 有 logger
