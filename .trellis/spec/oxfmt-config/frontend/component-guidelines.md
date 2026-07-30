# @vben/oxfmt-config "Component" Style - Config Object

> 无 Vue 组件。这里的 "组件" 是带类型的配置对象。

## 模式

```ts
import type { Linter } from "eslint";
export const config: Linter.Config[] = [
  /* config entries */
];
```

## 用法

```ts
import { config as eslintConfig } from "@vben/oxfmt-config";
export default [
  ...eslintConfig,
  // app-specific overrides
];
```

## 禁止

- 不要添加带副作用的函数
- Don't add CLI/runtime code
- 不要引入运行时依赖——保持零依赖
