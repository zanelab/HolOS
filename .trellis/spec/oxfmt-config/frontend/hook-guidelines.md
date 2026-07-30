# oxfmt-config: No Hooks

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
import baseConfig from 'oxfmt-config';
const cfg = ref(baseConfig);  // makes no sense
```

## Forbidden

- ❌ 不要在 `oxfmt-config` 加 Vue / Pinia
- ❌ 不要 add runtime changes
- ❌ 不要 use `useXxx` exports
- ❌ 不要 mutate config at runtime (read-only reference)
