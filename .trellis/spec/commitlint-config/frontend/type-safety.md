# @vben/commitlint-config Type Safety

> Strict-mode TS, leaf package.

## TS Config

```json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Enables `strict`, `noUnusedLocals`, `verbatimModuleSyntax`.

## Required Patterns

### 1. Use UserConfig generic from @commitlint/types

```ts
import type { UserConfig } from '@commitlint/types';

export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix']],
  },
} satisfies UserConfig;
```

### 2. Rules keyed by exact strings

```ts
rules: {
  'type-enum': [2, 'always', [...]],
  'subject-empty': [2, 'never'],
  'header-max-length': [2, 'always', 72],
}
```

### 3. parserOpts for non-conventional header

```ts
parserPreset: {
  parserOpts: {
    headerPattern: /^(\w+)(?:\(([^\)]*)\))?!?:\s*(.+)$/,
    headerCorrespondence: ['type', 'scope', 'subject'],
    referenceActions: ['break', 'close'],
  },
},
```

## Type Imports

```ts
import type { UserConfig, RuleConfigSeverity } from '@commitlint/types';
import type { ParserPreset } from '@commitlint/types';
```

## Rule Severity Levels

```ts
type RuleConfigSeverity = 0 | 1 | 2;
// 0 = disabled
// 1 = warning
// 2 = error
```

## Forbidden

- ❌ 不要用 `any` for rules dict — declare explicit type
- ❌ 不要 modify rule values dynamically(必须是 literal)
- ❌ 不要 disable types: 不要 add `'type-enum': [0, ...]`
- ❌ 不要 add Vue/Pinia imports(only @commitlint/types)
- ❌ 不要 use `as` cast to silence errors in this file
- ❌ 不要 disable strict mode per-file
- ❌ 不要 add `skipLibCheck: true` per-file(虽然 base 启用)
