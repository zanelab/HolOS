# typings 组件规范

**Expected package:** @vben-core/typings — generic TS types (planned)

> **PLACEHOLDER DOCS** — 本包 does not exist in the workspace at this time. The expected structure and patterns below are based on `vben v5.7.0` conventions. 替换这些文件 real content when package 添加后.

## 预期约定

- Vue 3 +  TypeScript 严格模式 (when applicable)
- Single barrel at `src/index.ts` (re-export public API)
- Tree-shake friendly (named exports only)
- Tests in `__tests__/` alongside source

## 示例 (synthetic)

```ts
// src/index.ts
export * from './helpers';
export { useXxx } from './use-xxx';
```

## 禁止

- 不要 implement against this placeholder before the real package exists
- 不要 deep-import from `@vben/typings/internal/*` (package does not exist)
- 不要 add real source files under `internal/<phantom>/`