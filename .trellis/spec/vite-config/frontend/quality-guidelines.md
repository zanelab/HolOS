# @vben/vite-config Quality Guidelines

> Quality is enforced by **tsdown build + pnpm typecheck + arcanum CI**.
> Source verified against `internal/vite-config/src/` v5.7.0.

## TS 风格 (强制)

- **4-space indent** —— `.ts/.json` 文件统一
- **single quotes** —— TS source 用单引号,JSON 用双引号
- **no semicolon bias** —— verified 仓库用 `;`(参考 `application.ts`)
- **`async/await` over `.then()`** —— plugin 函数全 async
- **arrow fn 默认** —— `() => Promise<...>`,named export 仅顶层用

## Build pipeline (verified)

```ts
// tsdown.config.ts (verified)
import { defineConfig } from 'tsdown';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm'],
  dts: true,
  clean: true,
  // 单 file 输出 — dist/index.mjs + dist/index.d.ts
});
```

## Linting

```jsonc
// 内 lint config extends @vben/eslint-config + oxlint
{
  "extends": ["@vben/eslint-config"],
  "rules": {
    "unused-imports/no-unused-imports": "error"
  }
}
```

## 测试矩阵

| 文件族                       | 谁测试                       | 覆盖率如何                          |
| ---------------------------- | ---------------------------- | ----------------------------------- |
| `src/config/**`              | `apps/*/build` (manual)      | 由 apps 集成 smoke test             |
| `src/plugins/*`              | manual via apps dev/build    | 集成测试,无 unit                    |
| `src/typing.ts`              | 100% by `tsc`                | strict + verbatimModuleSyntax       |
| `src/options.ts`             | smoke by app boot            | PWA manifest 渲染                    |
| `src/utils/env.ts`           | manual via apps dotenv       | 已知 ENV configs fixture            |

## Conventions

- **`dist/` 由 tsdown 生成** —— 永远 gitignore,绝不手编
- **`src/index.ts` 5 行内** —— 集中 re-export,无逻辑
- **plugin 必须返回数组** —— 即便只有 1 个 plugin hook
- **options 是 plain object** —— 不 class,不 immer
- **TYPE re-exports 必须用 `export type * from`** —— `verbatimModuleSyntax` 兼容
- **`enforce`, `apply`, `name` 必填** 在 plugin object 上

## Naming

- file name: kebab-case for plugins (`extra-app-config.ts`)
- file name: camelCase for configs (`application.ts`)
- exported fn: `define{Category}`, `vite{Name}Plugin`, `load{Condition}Plugins`
- exported types: `XxxPluginOptions` 或 `XxxConfig`

## 修改 plugin 的 check list

```text
[ ] src/plugins/{name}.ts
[ ] src/plugins/index.ts export
[ ] src/typing.ts options shape
[ ] src/config/application.ts 默认值
[ ] (若 ENV) src/utils/env.ts 解构
[ ] (若 default) src/options.ts
[ ] .trellis/spec/vite-config/frontend/{file}.md 文档同步
[ ] pnpm --filter @vben/vite-config run build 通过
```

## Forbidden

- ❌ 不要修改 `tsdown.config.ts` 临时构建 flags —— 由 CI 决定
- ❌ 不要在 plugin 调用 `console.log` (用 `vitePrintPlugin`)
- ❌ 不要让 plugin name 与 unplugin-vue-components 等冲突
- ❌ 不要把 ENV 默认值改硬编码 —— 应来自 `loadAndConvertEnv`
- ❌ 不要加 `'use strict'` directive(默认 TS 已 strict)
- ❌ 不要给 `defineConfig` 加 sync 路径 —— 必须 async
