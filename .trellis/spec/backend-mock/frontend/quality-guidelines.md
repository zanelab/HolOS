# @vben/backend-mock Quality Guidelines

> Mock-only strict-mode server code.

## Coding Style

- 4 spaces TS indent
- Single quotes
- No semicolons
- Async/await throughout endpoint handlers

## Filename Convention

| Pattern | Example | Maps To |
|---|---|---|
| `<resource>.<method>.ts` | `login.post.ts` | POST /api/login |
| `[param].<method>.ts` | `[id].get.ts` | GET /api/:id |
| `<group>/<resource>.<method>.ts` | `auth/codes.ts` | GET /api/auth/codes |

## Naming

- 路由文件:`kebab-case`
- 内部 types:`PascalCase`,前缀可选(`LoginRequest`, `MockUser`)
- Imports: `@vben/...` workspace names

## Pattern Examples

### Error handling

```ts
// ✅ Good
throw createError({ statusCode: 401, message: 'Invalid credentials' });

// ❌ Bad
return { ok: false, error: 'Invalid credentials' };
```

### Type-safe body

```ts
// ✅ Good
const body = await readBody<LoginRequest>(event);

// ❌ Bad
const body = await readBody(event);  // 类型推断 any
```

### Validation

```ts
if (!body.username || !body.password) {
  throw createError({ statusCode: 400, message: 'Missing fields' });
}
```

## Pre-commit

- OxLint
- OxFmt (format on commit)
- ESLint flat config
- commitlint (`feat():` / `fix():` / `chore():`)
- Vitest (test runner on backend-mock)

## Forbidden

- ❌ 不要用 Express/Koa — Nitro h3 only
- ❌ 不要用 Generators (`yield`) — Nitro is async/await
- ❌ 不要 add real DB — keep mock-only
- ❌ 不要 commit `.env` or secret files (即使是 mock,still risky)
- ❌ 不要 console.log for debug — Nitro has `logger.useLogger()`
- ❌ 不要用 Cookies — Bearer token only
- ❌ 不要用 process.env for runtime config (nitro runtime config 才是正道)
- ❌ 不要 commit `node_modules/`, `dist/`, `.vite/`

## Run Command

```bash
pnpm dev:backend-mock    # starts Nitro on localhost:5320
```

## Lint / Typecheck

```bash
pnpm typecheck
pnpm lint
```
