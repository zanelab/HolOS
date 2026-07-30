# @vben/lint-configs Directory Structure

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
