# @vben/commitlint-config Directory Structure

> Config-only package consumed by commitlint CLI via `commitlint.config.mjs`
> symlink or workspace alias. Source verified against
> `internal/lint-configs/commitlint-config/` v5.7.0.

## 目录树 (verified)

```
@vben/commitlint-config/                       # workspace: internal/lint-configs/commitlint-config/
├── package.json                              # name "@vben/commitlint-config" v5.7.0
├── index.mjs                                 # 直接 commit config —— default export
├── dist/                                     # tsdown 副产物,gitignored
│   ├── index.mjs                              # copy of index.mjs (构建 sync)
│   └── (...)
└── node_modules/
```

注意:`commitlint-config` 不同其他 lint-config 子包——它只发 1 个
**`index.mjs`**,没有 `src/`。 因为 commitlint 配置仅 default export 一个
object,无类型,无 build 复杂度。

## 关键文件 (verified)

`package.json`:

```json
{
  "name": "@vben/commitlint-config",
  "version": "5.7.0",
  "private": true,
  "type": "module",
  "files": ["dist"],
  "main": "./index.mjs",
  "module": "./index.mjs",
  "exports": {
    ".": {
      "import": "./index.mjs",
      "default": "./index.mjs"
    }
  },
  "dependencies": {
    "@commitlint/cli": "catalog:",
    "@commitlint/config-conventional": "catalog:",
    "@vben/node-utils": "workspace:*",
    "commitlint-plugin-function-rules": "catalog:",
    "cz-git": "catalog:",
    "czg": "catalog:"
  }
}
```

`commitlint.config.mjs` (仓库根, 引用本包):

```js
export { default } from '@vben/commitlint-config';
```

## Patterns

- **1 file, 1 default export** —— `index.mjs` 唯一 source,export 一个
  `UserConfig`(cz-git)object
- **0 个 `src/`** —— 复杂度过低,不需要 `src/` + `dist/` 隔离
- **`commitlint-plugin-function-rules`** —— 用于 `scope-enum` 动态校验
- **`getPackagesSync()`** —— 从 `@vben/node-utils` 读所有 workspace 包名
  → 自动构建 scope allowlist

## Conventions

- **`private: true`** —— 不发到 npm,只能 workspace 引用
- **build via tsdown** —— 与其他 lint 包一致
- **`type: "module"`** —— ESM only
- **`compatibility`** —— 同时配置 **commitlint rules** (rules object) +
  **cz-git prompts** (UserConfig.prompt)
- **scope auto-derive** —— 从 `git status --porcelain` 解析 modified file

## Naming

- 内文件 `index.mjs` —— 唯一 source
- 顶层只有一个 default export:`userConfig`(`@type {import('cz-git').UserConfig}`)
- aliases 全小写 (`b`, `c`, `f`, `r`, `s`) 在 prompt.alias

## Forbidden

- ❌ 不要在此包加 `src/` 子目录或拆多个 .mjs 文件
- ❌ 不要把 `commitlint.config.mjs` 留在仓库根以外的目录 —— workspace
- ❌ 不要写 sync `fs.readFile` —— 用 `getPackagesSync`(已 cache)
- ❌ 不要 hardcode list 的 scope 在 `scope-enum` —— 用 `getPackagesSync()`
- ❌ 不要移除 `commitlint-plugin-function-rules` —— scope allowlist 依赖它
- ❌ 不要在 `UserConfig` 加非 commitlint 字段(像 eslint options)
