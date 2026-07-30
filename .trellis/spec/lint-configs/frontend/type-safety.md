# lint-configs sub-package Type Safety

> Strict-mode TS for Lint flat config.

## TS Config

```json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Enables `strict`, `noUnusedLocals`, `verbatimModuleSyntax`.

## Required Patterns

### 1. Re-export flat config

```ts
import type { Linter } from 'eslint';

// 类型 strict 验证 flat config shape
const config: Linter.Config[] = [
  {
    rules: { /* ... */ },
  },
];

export default config;
```

### 2. Type the ParserOptions

```ts
import type { ParserOptions } from '@typescript-eslint/parser';

const parserOptions: ParserOptions = {
  ecmaVersion: 'latest',
  sourceType: 'module',
  project: './tsconfig.json',
};
```

### 3. Rule with Options

```ts
rules: {
  '@typescript-eslint/consistent-type-imports': ['error', { prefer: 'type-imports' }],
  'vue/no-v-html': ['error', { allow: ['::v-deep', '::v-slotted'] }],
}
```

## Type-Safe Rule Keys

```ts
import type { Linter } from 'eslint';

// Lint types expose rule keys as a literal union
type RuleKey = keyof Linter.RulesRecord;  // string
```

Lint type system catches typos in rule keys.

## Forbidden

- ❌ 不要用 `any` for rule values
- ❌ 不要 disable strict mode per-file
- ❌ 不要 use `as` cast to suppress errors
- ❌ 不要 add Vue / Pinia imports to this package
- ❌ 不要 bundle parse plugin — declare as app deps
- ❌ 不要 load config at runtime in `index.ts` (CI / editor do it)
- ❌ 不要 add `skipLibCheck: true` per-file
