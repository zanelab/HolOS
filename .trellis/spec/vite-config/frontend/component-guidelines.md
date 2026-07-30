# @vben/vite-config "Component" Style - Config Object

> 无 Vue 组件。 "Components" are typed config objects.

## 模式

```ts
import type { Linter } from "eslint";
export const config: Linter.Config[] = [
  /* config entries */
];
```

## 用法

```ts
import { config as eslintConfig } from "@vben/vite-config";
export default [
  ...eslintConfig,
  // app-specific overrides
];
```

## 禁止

- Don't add side-effect functions
- Don't add CLI/runtime code
- Don't import runtime deps - zero-dep
