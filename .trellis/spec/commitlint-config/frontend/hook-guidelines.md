# @vben/commitlint-config: No Hooks

> This is a config package, no Vue hooks.

## Where to enforce rules

- **lefthook pre-commit** at workspace root: reads commitlint config, validates commit message
- **CI pipeline** (optional): runs `pnpm commitlint --from=HEAD~1` on PR

```yaml
# .lefthook.yml (root)
commit-msg:
  commands:
    commitlint:
      run: pnpm exec commitlint --edit
```

## 实际 Use Cases

```bash
# Validate last commit
pnpm exec commitlint --from=HEAD~1 --to=HEAD

# Validate commit message in editor
pnpm exec commitlint --edit
```

The `@vben/commitlint-config` package is **consumed** via `commitlint.config.ts` in each app, so the rules apply app-wide via:

```ts
// apps/web-holos/commitlint.config.ts
import commitlintConfig from '@vben/commitlint-config';
export default commitlintConfig;
```

## Built-ins (this package exports)

This package has:
- 1 default export: configuration object
- No `useXxx` hooks

## Forbidden

- ❌ 不要在 `@vben/commitlint-config` 添加 Vue / Pinia imports
- ❌ 不要 add `export * from './hooks'` (this package has no hooks)
- ❌ 不要 add runtime config loading — keep it static
- ❌ 不要 bypass via `--no-verify` (rare; manually annotate in commit body)
