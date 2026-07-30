# @vben/commitlint-config Type Safety

> 严格模式 TS.

```ts
import type { Linter } from 'eslint';
export const config: Linter.Config[] = [...];
```

## 禁止

- Don't disable strict mode
- 不要使用 any
