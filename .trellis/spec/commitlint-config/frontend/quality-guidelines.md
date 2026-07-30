# @vben/commitlint-config Quality Guidelines

> Strict-mode TS, config object.

## 代码风格

```ts
import type { UserConfig } from '@commitlint/types';

export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [...types]],
    'type-max-length': [2, 'always', 72],
  },
} satisfies UserConfig;
```

## Rules Format

每个规则: `[level, applicability, value]`
- level: `0` (disable) / `1` (warn) / `2` (error)
- applicability: `'always'` / `'never'`
- value: rule-specific config

## Naming

| Thing | Convention |
|---|---|
| Type (commit type) | lowercase noun (feat, fix, docs, refactor, perf) |
| Scope | lowercase package name (`web-holos`, `router`, `locales`) |
| Rule key | camelCase + dashes (`type-enum`, `header-max-length`) |

## Patterns

### Conventional 11 types

```ts
'type-enum': [2, 'always', [
  'feat', 'fix', 'docs', 'style', 'refactor', 'perf',
  'test', 'build', 'ci', 'chore', 'revert',
]],
```

### Header length limits

```ts
'type-min-length': [2, 'always', 10],     // minimum type char count
'type-max-length': [2, 'always', 72],    // maximum type char count
'header-max-length': [2, 'always', 72],  // entire header (<= 72)
'subject-min-length': [2, 'always', 10], // subject >= 10 chars
'subject-max-length': [2, 'always', 72],
```

## Test

Configs can be unit-tested:

```ts
import { expect, it } from 'vitest';
import { default as commitlintConfig } from '../index';

it('forbids uppercase type', () => {
  const rules = commitlintConfig.rules ?? {};
  expect(rules['type-case']).toEqual([2, 'always', 'lower-case']);
});
```

## Pre-commit Hooks

- commitlint --edit (this config)
- OxLint, OxFmt, ESLint (per usual)

## Forbidden

- ❌ 不要 modify type-enum 列表 — 11 types is convention
- ❌ 不要添加 type length > 72 (Debian + GitHub convention)
- ❌ 不要 disable rules with `[0, ...]` except documented cases
- ❌ 不要 add @typescript-eslint/no-explicit-any — config uses type assertion
- ❌ 不要 add Vue / React imports to this package
- ❌ 不要 make this package async/IO
- ❌ 不要 commit `.commitlintrc.json` in apps — point to this package
