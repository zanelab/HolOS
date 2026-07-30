# shared Component Guidelines

**Expected package:** @vben-core/shared — runtime constants (planned)

> **PLACEHOLDER DOCS** — This package does not exist in the workspace at this time. The expected structure and patterns below are based on `vben v5.7.0` conventions. Replace these files with real content when the package is added.

## Expected Conventions

- Vue 3 + TypeScript strict mode (when applicable)
- Single barrel at `src/index.ts` (re-export public API)
- Tree-shake friendly (named exports only)
- Tests in `__tests__/` alongside source

## Example (synthetic)

```ts
// src/index.ts
export * from './helpers';
export { useXxx } from './use-xxx';
```

## Forbidden

- Do not implement against this placeholder before the real package exists
- Do not deep-import from `@vben/shared/internal/*` (package does not exist)
- Do not add real source files under `internal/<phantom>/`