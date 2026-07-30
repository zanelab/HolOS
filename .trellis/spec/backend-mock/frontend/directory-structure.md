# @vben/backend-mock Directory Structure

> Real layout for `apps/backend-mock/`. Source verified 2026-07-30.

## Purpose

`@vben/backend-mock` is the **Nitro-based mock backend** that ships
alongside the workspace. It hosts the demo API endpoints the web-*
apps hit during dev: login, user info, menus, tables, demo data,
timezone, system tables. It is **not** a production backend — it lives
in `apps/` (not `packages/`) and is dev-only.

## 目录树 (verified from `apps/backend-mock/`)

```
backend-mock/                       # workspace: apps/backend-mock/
├── package.json                    # name "@vben/backend-mock" v5.7.0
├── nitro.config.ts                 # CORS, dev/prod error handler
├── tsconfig.json + tsconfig.build.json
├── error.ts                        # NitroErrorHandler — prints stack
├── README.md
├── api/                            # HTTP endpoints (file-based routing)
│   ├── auth/
│   │   ├── codes.ts                # GET /api/auth/codes
│   │   ├── login.post.ts           # POST /api/auth/login
│   │   ├── logout.post.ts
│   │   └── refresh.post.ts
│   ├── demo/
│   │   └── bigint.ts
│   ├── menu/
│   │   └── all.ts                  # GET /api/menu/all
│   ├── system/
│   │   ├── dept/
│   │   ├── menu/
│   │   ├── role/
│   │   └── user/
│   ├── table/
│   │   └── list.ts
│   ├── timezone/
│   │   ├── getTimezone.ts
│   │   ├── getTimezoneOptions.ts
│   │   └── setTimezone.ts
│   ├── user/
│   │   └── info.ts                 # GET /api/user/info
│   ├── status.ts                   # GET /api/status?status=NNN
│   ├── test.get.ts                 # GET /api/test
│   ├── test.post.ts                # POST /api/test
│   └── upload.ts
├── middleware/
│   └── 1.api.ts                    # CORS + 模拟环境禁用写
├── routes/
│   └── [...].ts                    # 根目录广告 / 落地页
└── utils/
    ├── cookie-utils.ts             # setRefreshTokenCookie / clearRefreshTokenCookie
    ├── jwt-utils.ts                # generateAccessToken / verifyAccessToken
    ├── mock-data.ts                # MOCK_USERS, MOCK_MENUS, MOCK_TABLE
    ├── response.ts                 # useResponseSuccess / useResponseError / forbiddenResponse
    └── timezone-utils.ts
```

## Real source (verified)

```ts
// apps/backend-mock/nitro.config.ts
import errorHandler from './error';

process.env.COMPATIBILITY_DATE = new Date().toISOString();
export default defineNitroConfig({
  devErrorHandler: errorHandler,
  errorHandler: '~/error',
  routeRules: {
    '/api/**': {
      cors: true,
      headers: {
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Headers': '...',
        'Access-Control-Allow-Methods': 'GET,HEAD,PUT,PATCH,POST,DELETE',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Expose-Headers': '*',
      },
    },
  },
});
```

## Conventions

- **File-based routing** — URL path mirrors file path.
- **Filename convention**: `<resource>.<method>.ts` for HTTP-method-
  specific handlers (`test.get.ts`, `login.post.ts`); plain `<name>.ts`
  for method-agnostic.
- **Folder structure** — `api/<resource>/<handler>.ts` (e.g.,
  `api/auth/login.post.ts`).
- **Middleware** is folder-based and ordered by filename prefix.
- **Helpers** in `utils/` — `~/utils/response`, `~/utils/jwt-utils`,
  `~/utils/mock-data`, `~/utils/cookie-utils`.
- **Run via** `pnpm dev:backend-mock` (port 5320 by default).

## Naming

| Thing | Convention | Example |
|---|---|---|
| Folder | `<resource>/` | `auth/`, `user/`, `menu/` |
| Handler | `<name>.<method>.ts` | `login.post.ts`, `test.get.ts` |
| Generic handler | `<name>.ts` | `info.ts`, `all.ts` |
| Middleware | `<order>.<name>.ts` | `1.api.ts` |
| Utility | `<name>-utils.ts` | `jwt-utils.ts` |

## Forbidden

- ❌ 不要 use Express — Nitro + h3 only
- ❌ 不要 这里放真实 authentication — mock-only
- ❌ 不要 add real database — in-memory `MOCK_*` only
- ❌ 不要 bypass `useResponseSuccess` / `useResponseError` — uniform shape
- ❌ 不要 mutate `MOCK_USERS` at runtime — treat as immutable
- ❌ 不要 ship `*.sql` / connection strings — there is no DB
- ❌ 不要 add `tsx` scripts — Nitro handles ts compilation
