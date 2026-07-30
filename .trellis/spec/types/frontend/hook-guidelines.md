# @vben/types: No Hooks

> 纯常量 / 类型包。无 Vue Hooks。

应用通过自身代码中的 composables 引用：

```ts
import { usePreferences } from '@vben/preferences';
import { LAYOUTS } from '@vben/types';
```

## 禁止

- Don't add Vue hooks here
- 不要添加响应式状态
