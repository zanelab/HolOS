# @vben/node-utils Quality Guidelines

> Strict-mode TS, 4-space, single quotes, max line 120.

## Code Style

- **4 spaces** indent
- **Single quotes** for strings
- **No trailing comma** in multiline (matches the repo's ESLint config)
- **Max line length**: 120 chars
- **Trailing newline** at end of every file
- **Strict mode** TS — no `any`, no implicit `any`

## Naming

| Thing | Convention | Example |
|---|---|---|
| Function helper file | `kebab-case.ts` | `format-bytes.ts` (despite filename `formatter.ts`) |
| Function | `verbNoun` | `formatBytes`, `hashContent` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Type | `PascalCase` | `FormatOptions` |
| Test file | `<unit>.test.ts` | `formatter.test.ts` |

## Tests (in `__tests__/`)

```bash
pnpm --filter @vben/node-utils test
```

Pattern: **Vitest**, **one describe per source file**, **unit-level coverage** of all exported functions.

## Forbidden

- ❌ Don't import `lodash` or any utility lib — this package is **deliberately lean**.
- ❌ Don't add `console.log` to helpers — keep them side-effect free.
- ❌ Don't use `process.cwd()` (or any cwd-derived path) inside a helper — let the caller pass a base directory in.
- ❌ Don't add a `dist/` directory to git — `scripts/stub.mjs` provides a fake `dist/index.mjs` for tsx consumers.
- ❌ Don't introduce new dependencies without first checking whether the helper belongs in this package (it's a leaf utility — most things shouldn't).
