# @vben/backend-mock Directory Structure

> Real layout for `apps/backend-mock/`. Source verified 2026-07-30.

## 目录树

```
@vben/backend-mock/                 # workspace: apps/backend-mock/
├── package.json                    # name "@vben/backend-mock" v5.7.0
├── nitro.config.ts                 # Nitro server config
├── tsconfig.json
├── tsconfig.build.json             # 用于 build dist
├── error.ts                        # h3 createError helpers
├── README.md
├── .env                            # local mock env
└── api/                            # ❗ 直接 api/, NOT src/api/
    ├── auth/                       # /api/auth/*
    │   ├── codes.ts                # GET  — 验证 codes
    │   ├── login.post.ts           # POST — login
    │   ├── logout.post.ts          # POST — logout
    │   └── refresh.post.ts         # POST — refresh token
    ├── demo/                       # demo endpoints
    │   ├── bigint.ts
    │   └── ...
    ├── menu/
    │   └── all.ts                  # /api/menu/all — used by router/access.ts
    ├── system/
    │   └── ...
    ├── table/
    │   └── list.ts
    ├── timezone/
    ├── user/
    └── status.ts                   # GET /api/status — health
```

## 真实源码参考 (verified)

`apps/backend-mock/api/auth/login.post.ts`:

```ts
import { defineEventHandler, readBody, createError } from 'h3';

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

  if (!body.username || !body.password) {
    throw createError({
      statusCode: 400,
      message: 'Missing username or password',
    });
  }

  if (body.username !== 'vben' || body.password !== 'vben123') {
    throw createError({
      statusCode: 401,
      message: 'Invalid credentials',
    });
  }

  return {
    access_token: 'mock-access-token-' + Date.now(),
    refresh_token: 'mock-refresh-token-' + Date.now(),
    token_type: 'Bearer',
    expires_in: 3600,
  };
});
```

`apps/backend-mock/api/menu/all.ts`:

```ts
import { defineEventHandler } from 'h3';

interface MenuItem {
  id: string;
  path: string;
  title: string;
  icon?: string;
  children?: MenuItem[];
}

export default defineEventHandler((event): MenuItem[] => {
  // Mock: 静态 menu tree
  return [
    {
      id: 'dashboard',
      path: '/dashboard',
      title: '概览',
      icon: 'lucide:layout-dashboard',
      children: [
        { id: 'analytics', path: '/dashboard/analytics', title: '分析页' },
      ],
    },
    // ...
  ];
});
```

## Conventions

- **直接 api/ 目录** (非 src/api/) — Nitro auto-discovers
- **Filename convention**: `<resource>.<method>.ts`
  - `login.post.ts` → POST /api/login
  - `codes.ts` → GET /api/codes
  - `all.ts` → GET /api/all
- **use `defineEventHandler`** from `h3` — Nitro's HTTP layer
- **Mock data only** — no real DB, no real auth
- **In-memory state** — 每次 server restart 数据 丢失

## Real App Integration

App consumption 通过 `@vben/request`:

```ts
// apps/web-tdesign/src/api/request.ts
import { createRequestClient } from '@vben/request';

export const requestClient = createRequestClient({
  baseURL: '/api',
  // 前端走 vite proxy 到 localhost:5320
});
```

```ts
// Usage in a view
const userInfo = await requestClient.post('/auth/login', {
  username: 'vben',
  password: 'vben123',
});
```

## Forbidden

- ❌ 不要加 real DB / Redis — Nitro mock 保持 in-memory only
- ❌ 不要 Express / Koa middleware — 用 Nitro h3 handlers
- ❌ 不要持久化 auth tokens 到 disk (security)
- ❌ 不要 import `@vben/web-*` packages — 这是 server-side,不依赖 app
- ❌ 不要 create sources/ 目录 — 直接 api/ 顶级
- ❌ 不要 commit `.env` — 即使 mock secrets
