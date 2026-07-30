# oxfmt-config Directory Structure

> ESLint flat config for HolOS monorepo.

## 目录树

```
oxfmt-config/                 # workspace: internal/lint-configs/eslint-config/
├── package.json                     # name "oxfmt-config" v5.7.0
├── tsconfig.json
└── src/
    ├── index.ts                     # 公开 barrel — re-exports flat config
    └── rules/                        # per-rule modules (optional)
```

## 实际源码参考

Flat config 结构 (verified):

```ts
// internal/lint-configs/eslint-config/index.ts
import tseslint from 'typescript-eslint';
import vue from 'eslint-plugin-vue';
import oxlint from 'eslint-plugin-oxlint';

export default tseslint.config(
  // TypeScript rules
  ...tseslint.configs.recommendedTypeChecked,
  // Vue 3 rules (vben apps use Vue 3)
  ...vue.configs['flat/recommended'],
  // OxLint bridge (delegates rules to OxLint for speed)
  ...oxlint.configs['flat/recommended'],
  // Custom overrides
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/consistent-type-imports': ['error', { prefer: 'type-imports' }],
      'vue/multi-word-component-names': 'off',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
);
```

## Conventions

- **Flat config** (`.eslintrc.json` legacy deprecated)
- **Type-checked** TypeScript rules via `typescript-eslint`
- **Vue 3** rules via `eslint-plugin-vue`
- **OxLint bridge** — fast lint delegated to OxLint binary
- **Custom rule severity** — error / warn / off per rule

## Usage in apps

```ts
// apps/web-holos/eslint.config.ts
import baseConfig from 'oxfmt-config';

export default [
  ...baseConfig,
  // App-specific overrides
  {
    files: ['scripts/**/*.ts'],
    rules: { 'no-console': 'off' },
  },
];
```

## Forbidden

- ❌ 不要使用 .eslintrc.* 旧 config 格式 — flat config only
- ❌ 不要 disable TypeScript rules without documented reason
- ❌ 不要 add Vue 2 rules — Vben is Vue 3 only
- ❌ 不要 commit generated `.eslintcache` to git
- ❌ 不要 use ESLint for auto-formatting — OxFmt does that
- ❌ 不要 import eslint-plugin-vue v8.x — need v9+ for flat config
