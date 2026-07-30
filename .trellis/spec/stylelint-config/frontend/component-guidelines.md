# stylelint-config "Component" Style — Flat Config

> ESLint flat config = a flat array of config objects.

## Pattern: Flat config array

```ts
import tseslint from 'typescript-eslint';
import vue from 'eslint-plugin-vue';
import oxlint from 'eslint-plugin-oxlint';

export default tseslint.config(
  // Step 1: Base TypeScript rules
  ...tseslint.configs.recommendedTypeChecked,
  // Step 2: Vue 3 plugin
  ...vue.configs['flat/recommended'],
  // Step 3: OxLint bridge (runs OxLint over .ts files)
  ...oxlint.configs['flat/recommended'],
  // Step 4: Custom rules
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/consistent-type-imports': ['error', { prefer: 'type-imports' }],
      'vue/multi-word-component-names': 'off',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
  // Step 5: Per-file overrides
  {
    files: ['*.config.{js,ts}', 'scripts/**/*.ts'],
    rules: { 'no-console': 'off' },
  },
);
```

## Real Usage

```ts
// apps/web-holos/eslint.config.ts (real)
import baseConfig from 'stylelint-config';

export default [
  ...baseConfig,
  {
    files: ['**/*.vue'],
    rules: { 'vue/no-v-html': ['error', { allow: ['::v-deep', '::v-slotted'] }] },
  },
];
```

## Tree-shake 验证

Apps 只需要 import default — tree-shaking 后只 bundle 实际使用规则。

## Forbidden

- ❌ 不要 export class-based configs — flat 数组 only
- ❌ 不要 include `globals:` — Vue 3 types + browser fields provided by tsplugin
- ❌ 不要在 flat config 用 `extends:` (deprecated)
- ❌ 不要 write `eslintrc: { root: true }` — flat config has no root concept
- ❌ 不要 bundle ESLint plugins — let apps `pnpm install` them
- ❌ 不要 have `parserOptions` in nested objects — top-level only
