# @vben/constants: No Hooks

> 纯常量 / 类型包。无 Vue Hooks。

应用通过自身代码中的 composables 引用：

```ts
import { usePreferences } from '@vben/preferences';
import { LAYOUTS } from '@vben/constants';
```

## 禁止

- 不要在此处添加 Vue hooks
- 不要添加响应式状态
