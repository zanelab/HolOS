# @vben/eslint-config: Static Config

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
