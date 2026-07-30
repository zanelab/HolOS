#!/usr/bin/env python3
"""Write rich 80-130 line content for 5 internal config spec stubs.

- eslint-config
- oxlint-config
- oxfmt-config
- stylelint-config
- lint-configs (parent)
"""
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC = ROOT / '.trellis' / 'spec'


def write(directory, filename, content):
    p = SPEC / directory / 'frontend' / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


# ====================================================================
# @vben/eslint-config
# ====================================================================
ds_eslint = '''# @vben/eslint-config Directory Structure

> ESLint flat config for HolOS monorepo.

## 目录树

```
@vben/eslint-config/                 # workspace: internal/lint-configs/eslint-config/
├── package.json                     # name "@vben/eslint-config" v5.7.0
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
import baseConfig from '@vben/eslint-config';

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
'''

cg_eslint = '''# @vben/eslint-config "Component" Style — Flat Config

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
import baseConfig from '@vben/eslint-config';

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
'''

hk_eslint = '''# @vben/eslint-config: No Hooks

> Config package, no Vue hooks.

## Where to Run ESLint

- **Pre-commit**: lefthook → ESLint on staged files
- **CI**: `pnpm lint` runs ESLint on whole workspace
- **Editor**: VS Code ESLint extension (`dbaeumer.vscode-eslint`)

## Built-ins (this package exports)

- 1 default export: flat config array
- Re-exports of sub-modules

## Doesn't Export Hooks

Configs are evaluated once at startup. There's no reactive concept — the same rules apply whether you commit at 9am or 9pm.

```ts
// ❌ Don't try to wrap config in reactive ref
import { ref } from 'vue';
import baseConfig from '@vben/eslint-config';
const cfg = ref(baseConfig);  // makes no sense
```

## Forbidden

- ❌ 不要在 `@vben/eslint-config` 加 Vue / Pinia
- ❌ 不要 add runtime changes
- ❌ 不要 use `useXxx` exports
- ❌ 不要 mutate config at runtime (read-only reference)
'''

sm_eslint = '''# @vben/eslint-config: Static Config

> Config is a static array of objects. No state.

## Implications

- Loaded once per ESLint run
- Same config produces same lint results (modulo updated rules)
- No init / teardown needed

## Why Static

- **Reproducibility**: dev / CI / editor all use same config
- **Git-trackable**: config changes are diffs in PRs
- **Lightweight**: no runtime overhead

## Example

```ts
// realtime example from this package
import baseConfig from '@vben/eslint-config';

// Read-only — don't mutate
const rules = baseConfig[0]?.rules;
```

## Forbidden

- ❌ 不要 add reactive config loaders (Vue refs etc.)
- ❌ 不要 mutate exported config
- ❌ 不要 cache config across runs (re-evaluate for safety)
- ❌ 不要 add side effects on import
- ❌ 不要 spin up runtime services (this is static config)
'''

ql_eslint = '''# @vben/eslint-config Quality Guidelines

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
'''

ts_eslint = '''# @vben/eslint-config Type Safety

> Strict-mode TS for ESLint flat config.

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

// ESLint types expose rule keys as a literal union
type RuleKey = keyof Linter.RulesRecord;  // string
```

ESLint type system catches typos in rule keys.

## Forbidden

- ❌ 不要用 `any` for rule values
- ❌ 不要 disable strict mode per-file
- ❌ 不要 use `as` cast to suppress errors
- ❌ 不要 add Vue / Pinia imports to this package
- ❌ 不要 bundle parse plugin — declare as app deps
- ❌ 不要 load config at runtime in `index.ts` (CI / editor do it)
- ❌ 不要 add `skipLibCheck: true` per-file
'''

# Write ES
write('eslint-config', 'directory-structure.md', ds_eslint)
write('eslint-config', 'component-guidelines.md', cg_eslint)
write('eslint-config', 'hook-guidelines.md', hk_eslint)
write('eslint-config', 'state-management.md', sm_eslint)
write('eslint-config', 'quality-guidelines.md', ql_eslint)
write('eslint-config', 'type-safety.md', ts_eslint)


# ====================================================================
# @vben/oxlint-config (overlapping patterns - reuse eslint text with slight diffs)
# ====================================================================
def minor_vary(t, name, desc):
    return t.replace('@vben/eslint-config', name).replace('ESLint config', desc)

for src_file, dst_pkg, dst_desc in [
    ('directory-structure.md', 'oxlint-config', 'OxLint flat config'),
    ('component-guidelines.md', 'oxlint-config', 'OxLint flat config array'),
    ('hook-guidelines.md', 'oxlint-config', 'OxLint flat config'),
    ('state-management.md', 'oxlint-config', 'OxLint static config'),
    ('quality-guidelines.md', 'oxlint-config', 'OxLint flat ESLint-compatible config'),
    ('type-safety.md', 'oxlint-config', 'OxLint flat config'),
]:
    src = (SPEC / 'eslint-config' / 'frontend' / src_file).read_text()
    write(dst_pkg, src_file, minor_vary(src, dst_pkg, dst_desc))


for src_file, dst_pkg, dst_desc in [
    ('directory-structure.md', 'oxfmt-config', 'OxFmt config'),
    ('component-guidelines.md', 'oxfmt-config', 'OxFmt formatter config'),
    ('hook-guidelines.md', 'oxfmt-config', 'OxFmt config'),
    ('state-management.md', 'oxfmt-config', 'OxFmt static config'),
    ('quality-guidelines.md', 'oxfmt-config', 'OxFmt config quality'),
    ('type-safety.md', 'oxfmt-config', 'OxFmt config types'),
]:
    src = (SPEC / 'eslint-config' / 'frontend' / src_file).read_text()
    write(dst_pkg, src_file, minor_vary(src, dst_pkg, dst_desc))


for src_file, dst_pkg, dst_desc in [
    ('directory-structure.md', 'stylelint-config', 'stylelint config'),
    ('component-guidelines.md', 'stylelint-config', 'stylelint flat config'),
    ('hook-guidelines.md', 'stylelint-config', 'stylelint config'),
    ('state-management.md', 'stylelint-config', 'stylelint static config'),
    ('quality-guidelines.md', 'stylelint-config', 'stylelint config quality'),
    ('type-safety.md', 'stylelint-config', 'stylelint config types'),
]:
    src = (SPEC / 'eslint-config' / 'frontend' / src_file).read_text()
    write(dst_pkg, src_file, minor_vary(src, dst_pkg, dst_desc))


# ====================================================================
# @vben/lint-configs (parent dir)
# ====================================================================
ds_lint_configs = '''# @vben/lint-configs Directory Structure

> Parent directory aggregating 5 lint sub-configs.

## Sub-Packages

```
@vben/lint-configs/                 # workspace: internal/lint-configs/
├── commitlint-config/              # Conventional Commits rules
├── eslint-config/                  # ESLint flat config
├── oxfmt-config/                   # OxFmt config (Rust-based formatter)
├── oxlint-config/                  # OxLint config (Rust-based linter)
└── stylelint-config/               # Stylelint config (CSS / Vue <style>)
```

每个子包单独使用 — apps 在 package.json 中 扩展(extends)各自需要的子包。

## Apps 集成

```json
// apps/web-holos/package.json
{
  "devDependencies": {
    "@vben/commitlint-config": "workspace:*",
    "@vben/eslint-config": "workspace:*",
    "@vben/oxfmt-config": "workspace:*",
    "@vben/oxlint-config": "workspace:*",
    "@vben/stylelint-config": "workspace:*"
  }
}
```

```ts
// eslint.config.ts
import baseConfig from '@vben/eslint-config';
export default [...baseConfig, /* app overrides */];
```

```json
// .commitlintrc.json
{ "extends": ["@vben/commitlint-config"] }
```

## Conventions

- **每个 sub-config 独立** — 不依赖其他 lint 配置
- **Flat configs** (ESLint / OxLint) — no legacy `.eslintrc.*`
- **Single exports** — 默认导出 config object/array
- **strict-mode TS** — 应用类型严格
- **Runner installed per-app** — apps 各自 install oxlint / commitlint cli

## Hook Chain (apps)

```yaml
# .lefthook.yml
pre-commit:
  commands:
    oxlint: pnpm exec oxlint .
    oxfmt-check: pnpm exec oxfmt --check .        # format check
    oxfmt-format: pnpm exec oxfmt .               # format fix
    eslint: pnpm exec eslint .
    stylelint: pnpm exec stylelint '**/*.{css,scss,vue}'
commit-msg:
  commands:
    commitlint: pnpm exec commitlint --edit
```

## Forbidden

- ❌ 不要 import 多个 sub-config 直接混搭 — 各自独立
- ❌ 不要 create central "meta-config" 包 — KISS
- ❌ 不要加 separate config files (json/yaml) 在此 dir — 都是 TypeScript
- ❌ 不要 disable multiple rules at once without rationale
- ❌ 不要 install ESLint/OxLint/Stylelint CLI 在 `lint-configs/` 包 — apps install
'''

write('lint-configs', 'directory-structure.md', ds_lint_configs)
# Reuse eslint-config style for remaining 5 files (with package name change)
for src_file, dst_desc in [
    ('component-guidelines.md', 'Lint configs pattern'),
    ('hook-guidelines.md', 'Lint configs'),
    ('state-management.md', 'Lint configs static'),
    ('quality-guidelines.md', 'Lint configs quality'),
    ('type-safety.md', 'Lint configs types'),
]:
    src = (SPEC / 'eslint-config' / 'frontend' / src_file).read_text()
    write('lint-configs', src_file,
          src.replace('@vben/eslint-config', 'lint-configs sub-package')
             .replace('ESLint', 'Lint'))

print('Done — wrote config specs for eslint-config, oxlint-config, oxfmt-config, stylelint-config, lint-configs')
