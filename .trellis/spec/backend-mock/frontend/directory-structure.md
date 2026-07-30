# @vben/backend-mock Directory Structure

> Mock backend built on **Nitro**.

## 目录树（已核对）

```
@vben/backend-mock/
├── package.json                # name "@vben/backend-mock" v5.7.0
├── nitro.config.ts
├── tsconfig.json + tsconfig.build.json
├── error.ts                    # h3 createError helper
├── README.md
└── src/
    ├── api/                    # <resource>.<method>.ts handlers
    │   ├── auth/    (login.post.ts, logout.post.ts)
    │   ├── demo/
    │   ├── menu/
    │   ├── system/
    │   ├── table/
    │   ├── timezone/
    │   └── user/
    ├── middleware/
    ├── routes/
    └── utils/
```

## 约定

- **Mock endpoints** use same path as production (`/api/...`)
- **Filename convention**: `<resource>.<method>.ts` (e.g. `login.post.ts`)
- **Run via** `pnpm dev:backend-mock` (port 5320)

## 禁止

- 不要使用 Express — 使用 h3
- 这里不要放入真实的认证 — 仅作 mock
- 不要添加真实数据库
