# @vben/node-utils Quality Guidelines

> 严格模式 TS, 4-space, single quotes, max line 120.

## 代码风格

- **4 个空格** 缩进
- 字符串使用 **单引号**
- **No trailing comma** in multiline (matches the repo's ESLint config)
- **最大行长**：120 个字符
- 每个文件末尾 **带换行**
- **严格模式** TS — no `any`, no implicit `any`

## 命名约定

| 项目 | 约定 | 示例 |
|---|---|---|
| Function helper file | `kebab-case.ts` | `format-bytes.ts` (despite filename `formatter.ts`) |
| Function | `verbNoun` | `formatBytes`, `hashContent` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Type | `PascalCase` | `FormatOptions` |
| Test file | `<unit>.test.ts` | `formatter.test.ts` |

## 测试s (in `__tests__/`)

```bash
pnpm --filter @vben/node-utils test
```

Pattern: **Vitest**, **one describe per source file**, **unit-level coverage** of all exported functions.

## 禁止

- ❌ Don't import `lodash` or any utility lib — 本包 is **deliberately lean**.
- ❌ Don't add `console.log` to helpers — keep them side-effect free.
- ❌ Don't use `process.cwd()` (or any cwd-derived path) inside a helper — let the caller pass a base directory in.
- ❌ Don't add a `dist/` directory to git — `scripts/stub.mjs` provides a fake `dist/index.mjs` for tsx consumers.
- ❌ 不要轻易引入新依赖，先检查该辅助是否属于 本包（本包是叶子工具，多数东西不该放进来）。
