# @vben/commitlint-config: Static Config

> Pure configuration object. No state.

## Implications

- Loaded at commit-time by commitlint CLI
- No init / no caching / no cleanup
- Same rules apply in dev / CI / release

## Why Static

- **Reproducibility**: every commit validation runs identical rules
- **Git history**: rules don't drift over time unless explicit bump
- **CI cache**: stateless rules = fast validation

## Examples

```ts
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const commitlintConfig: UserConfig = { /* ... */ };
export default commitlintConfig;
```

Each app loads it via:

```ts
// apps/web-holos/commitlint.config.cjs (or .ts)
module.exports = require('@vben/commitlint-config');
```

## Forbidden

- ❌ 不要在 commitlint-config 添加 mutable config loading
- ❌ 不要 wrap config in Vue reactive (不是 reactive state)
- ❌ 不要 export `ref(commitlintConfig)` — 这是 static
- ❌ 不要 cache parsed config — just re-read on each commit
- ❌ 不要 import config 在 runtime code(only in commitlint CLI / configs)
