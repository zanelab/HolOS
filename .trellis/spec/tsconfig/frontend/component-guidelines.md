# @vben/tsconfig "Component" Style - Config Object

> No Vue components. "Components" are typed config objects.

## Pattern

```ts
import type { Linter } from "eslint";
export const config: Linter.Config[] = [
  /* config entries */
];
```

## Usage

```ts
import { config as eslintConfig } from "@vben/tsconfig";
export default [
  ...eslintConfig,
  // app-specific overrides
];
```

## Forbidden

- Don't add side-effect functions
- Don't add CLI/runtime code
- Don't import runtime deps - zero-dep
