# lint-configs sub-package: No Hooks

> Config package, no Vue hooks.

## Where to Run Lint

- **Pre-commit**: lefthook → Lint on staged files
- **CI**: `pnpm lint` runs Lint on whole workspace
- **Editor**: VS Code Lint extension (`dbaeumer.vscode-eslint`)

## Built-ins (this package exports)

- 1 default export: flat config array
- Re-exports of sub-modules

## Doesn't Export Hooks

Configs are evaluated once at startup. There's no reactive concept — the same rules apply whether you commit at 9am or 9pm.

```ts
// ❌ Don't try to wrap config in reactive ref
import { ref } from 'vue';
import baseConfig from 'lint-configs sub-package';
const cfg = ref(baseConfig);  // makes no sense
```

## Forbidden

- ❌ 不要在 `lint-configs sub-package` 加 Vue / Pinia
- ❌ 不要 add runtime changes
- ❌ 不要 use `useXxx` exports
- ❌ 不要 mutate config at runtime (read-only reference)
