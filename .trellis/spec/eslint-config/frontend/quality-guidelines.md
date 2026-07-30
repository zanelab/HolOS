# @vben/eslint-config Quality Guidelines

> Flat ESLint config + TypeScript + Vue 3.

## Style

```ts
import tseslint from 'typescript-eslint';

export default tseslint.config(
  ...tseslint.configs.recommendedTypeChecked,
  { rules: { /* ... */ } },
);
```

## Rules Format

- Severity: `0` (off) / `1` (warn) / `2` (error)
- Array format: `[level, options]`
- Object form: `{ 'rule-name': level | [level, options] }`

## Naming

| Thing | Convention |
|---|---|
| Plugin | `eslint-plugin-*` (legacy) or `eslint-plugin-vue` |
| Flat config name | camelCase + `.config.ts` (`eslint.config.ts`) |
| Rules dictionary | kebab-case keys (`@typescript-eslint/no-explicit-any`) |

## Patterns

### Re-export from index

```ts
// eslint-config/index.ts
import baseConfig from './base';
export default baseConfig;
```

### Per-file overrides

```ts
export default tseslint.config(
  ...baseConfig,
  { 
    files: ['scripts/**/*.ts'],
    rules: { 'no-console': 'off' },
  },
);
```

## Pre-commit Hooks

- OxLint (fast linter, runs first)
- ESLint (detailed rules via `types:lint`)
- Stylelint (CSS / Vue `<style>`)

## Forbidden

- ❌ 不要 use legacy `.eslintrc.*` format — flat config only
- ❌ 不要 commit `.eslintcache`(已 gitignored)
- ❌ 不要 add parser-applicable rules in flat config dict (use `languageOptions`)
- ❌ 不要 use `overrides` — use top-level files in 数组 elements
- ❌ 不要 put Vue plugins for Vue 2 — Vue 3 only
- ❌ 不要 enable rules for non-existent code (e.g., `vue/no-v-html` ok with templates)
- ❌ 不要 commit npm-debug.log

## Lint Command

```bash
pnpm lint            # 全 workspace
pnpm typecheck       # TS check
```
