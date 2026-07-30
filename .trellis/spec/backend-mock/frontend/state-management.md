# @vben/backend-mock: In-Memory State

> Nitro Mock Server uses in-memory data only. No real persistence.

## Implications

- All data resets on server restart (`pnpm dev:backend-mock`)
- No database connection
- No file persistence unless for static demo JSON
- Tokens are JWT-like strings(issued on login,validated on protected endpoints)

## Real Mock State

```ts
// api/auth/codes.ts (real)
export default defineEventHandler(() => {
  // 静态 demo data
  return {
    codes: [
      { code: 'A001', label: 'Status 1' },
      { code: 'A002', label: 'Status 2' },
    ],
  };
});
```

## Mock JWT-like Auth Flow

```
1. Client POST /api/auth/login with { username, password }
2. Server check credentials (hard-coded 'vben' / 'vben123')
3. Return { access_token, refresh_token, expires_in }
4. Client stores tokens in @vben/stores's useAccessStore
5. Subsequent requests include Authorization: Bearer <token>
6. Each mock endpoint validates token heuristically (just non-empty)
```

## Why In-Memory Only

- **Demo-ready**: works without DB setup
- **Reset-able**: start fresh dev session by killing server
- **Mock-only**: production has real backend
- **Fast iteration**: no migration / seed scripts

## Demo Data Pattern

```ts
// api/menu/all.ts — mock menu tree
const MOCK_MENU = [
  {
    id: 'dashboard',
    path: '/dashboard',
    title: '概览',
    children: [
      { id: 'analytics', path: '/dashboard/analytics', title: '分析页' },
    ],
  },
];

export default defineEventHandler(() => MOCK_MENU);
```

## Forbidden

- ❌ 不要加 SQLite / Postgres / Redis 连接
- ❌ 不要 persist tokens to disk — security (even in mock)
- ❌ 不要用 file system (FS) for storage
- ❌ 不要 make mock state 全局 mutable across 多个 server 实例(如有)
- ❌ 不要用 cookies — Bearer token via Authorization header only
- ❌ 不要把 session data in Nitro context (无 state)
