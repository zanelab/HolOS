# @vben/tsconfig Directory Structure

> Config-only package consumed via workspace alias. Source verified 2026-07-30
> against `internal/tsconfig/` (v5.7.0).

## 目录树 (verified)

```
@vben/tsconfig/                       # workspace: internal/tsconfig/
├── package.json                      # name "@vben/tsconfig" v5.7.0, type:"module"
├── base.json                         # 严格 TS 基线,所有 variant 都 extends 此
├── library.json                      # extends base.json; declaration: true (库包)
├── node.json                         # extends base.json; types:["node"]
├── web-app.json                      # extends web.json; types:["vite/client", "@vben/types/global"]
└── web.json                          # extends base.json; jsx, DOM, bundler resolution
```

没有 `src/`,没有 `dist/`,没有 `tsconfig.json` —— 这些 JSON 由包消费者
(`apps/web-holos`、`packages/*`) 直接 `extends` 即可。

## 变体关系图 (cascade)

```
base.json                 # strict, ESNext, isolatedModules, noEmit, noUncheckedIndexedAccess
  ├─ library.json         # + declaration:true, noEmit:false, jsx:preserve
  ├─ node.json            # + lib:["ESNext"], types:["node"]
  └─ web.json             # + jsxImportSource:"vue", lib:DOM, moduleResolution:"bundler"
       └─ web-app.json    # + types:["vite/client","@vben/types/global"]
```

## Patterns

`package.json` (verified):

```json
{
  "name": "@vben/tsconfig",
  "version": "5.7.0",
  "private": true,
  "type": "module",
  "files": [
    "base.json",
    "library.json",
    "node.json",
    "web-app.json",
    "web.json"
  ],
  "dependencies": {
    "@vben/types": "workspace:*",
    "vite": "catalog:"
  }
}
```

App-side 消费方式 (apps/*/tsconfig.json 风格):

```jsonc
{
  "extends": "@vben/tsconfig/web-app.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*", "types/**/*"]
}
```

## Conventions

- **JSON files only** —— `.json` 文件可被 ts 直接 extends,无需 emit
- **`display` 字段** —— 每个 tsconfig 带 `"display"` 用于工具选择
- **`$schema`** —— 指向 json.schemastore.org/tsconfig 校验
- **包名 `@vben/tsconfig`** —— 永远不要改为 `@vben/ts-config` 等
- **`type: "module"`** —— 包本身 ESM,虽然只发 JSON

## Naming rules

- 变体命名:`<scope>.json` 全小写,`-` 分隔(`web-app` 而非 `webApp`)
- 字段名全小写(`compilerOptions`, `target`)
- 不要加 `tsconfig.json` 顶层文件 —— 会和变体冲突

## Forbidden

- ❌ 不要在包内加 `src/` 或 TypeScript 文件 —— 这是 JSON-only
- ❌ 不要加 `dist/`、`build step`、`publish script`
- ❌ 不要关掉 `"strict": true` —— `base.json` 是项目统一的 strict baseline
- ❌ 不要在 variant 里重新声明 `target`、`module` —— 应该 extends
- ❌ 不要新增 `"allowJs"` 等放宽字段 —— 5.7.0 默认纯 .ts
- ❌ 不要把 web-app.json 的 `types` 改成 `["@vben/types"]` —— `vite/client` 必须保留
