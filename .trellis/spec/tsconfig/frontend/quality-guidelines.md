# @vben/tsconfig Quality Guidelines

> Config-only package. Quality is measured by **(a)** JSON correctness,
> **(b)** strictness of compiler flags, **(c)** stable variant semantics.
> Source verified against `internal/tsconfig/` v5.7.0.

## JSON 风格 (强制)

- **2-space indent** —— JSON files, no tabs
- **trailing newline** —— EOF \n, single (不要 \r\n)
- **sort package.json field** —— verified: `package.json` ordered (name, version, type, files, ...)
- **double quotes only** —— 不允许单引号,即使在 comment 里也没用
- **comments via `$schema` 或 README** —— JSON 不能有 `//` 注释
- **no trailing comma** —— JSON spec 严格不允许

## TypeScript 严格性基线 (base.json)

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "noImplicitOverride": true,
    "noImplicitThis": true,
    "noUncheckedIndexedAccess": true,   // ← 关键,arr[i] 类型 T | undefined
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

任何 PR 修改以上任一字段 → **breaking change** → 必须 major bump + CHANGELOG。

## Validation workflow

```
1. pnpm --filter @vben/tsconfig run lint-json (内部 helper)
2. pnpm run typecheck --filter '@vben/*' (consumers 必须能通过)
3. IDE schema check (json.schemastore.org/tsconfig 自动)
4. ci pipeline: turbo run lint --filter=...
```

## Conventions

- **每个 variant 必须有 `display` 字段** —— IDE 选择器用
- **每个 variant 必须有 `$schema`** —— JSON Schema 校验
- **数组宽度建议 ≤ 8 项一行** —— 多于 8 换行
- **paths/aliases 不进 variant** —— 留给 app tsconfig override
- **`include` / `exclude` 不写在 variant** —— 留在 app tsconfig
- **category 命名:** `<stack>-<target>` (`web-app`, `node`, `library`)

## Naming

- 文件名 kebab-case + 全小写 (`web-app.json` 而非 `webApp.json` 或 `WebApp.json`)
- JSON 字段 camelCase (`moduleResolution` 而非 `module-resolution`)
- `display` 值 Title Case 多词 (`"Web Application"`)
- `dependencies` 用 catalog specifier (`"vite": "catalog:"` 已 verified)

## 测试矩阵

| 变体           | 谁消费                          | 测试策略                    |
| -------------- | ------------------------------- | --------------------------- |
| `base.json`    | 直接 extends by 所有 variant    | 由 variant 测试间接覆盖     |
| `library.json` | `packages/*` 库包               | `pnpm --filter ... build`   |
| `node.json`    | `internal/node-utils`           | `pnpm --filter ... build`   |
| `web.json`     | 包中含 Vue/JSX                  | `pnpm --filter ... build`   |
| `web-app.json` | `apps/web-*`                    | `pnpm --filter ... build`   |

## Forbidden

- ❌ 不要修改 `noUncheckedIndexedAccess: true` 或 `strict: true` —— breaking
- ❌ 不要在 variant 用 `// comments` —— JSON 严格
- ❌ 不要添加 `incremental` / `composite` 到 variant —— 让 turbo/tsc 自己决定
- ❌ 不要用 `"target": "es5"` 等过时 target —— 全栈已 `ESNext`
- ❌ 不要 split 成 multiple `compilerOptions.*.json` —— 5 variant 是上限
- ❌ 不要把 `tsconfig.json` 放包根目录(`internal/tsconfig/`) —— 与 variant 冲突
