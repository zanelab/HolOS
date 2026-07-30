# @vben/preferences: No Hooks

> Pure constants / types package. 无 Vue Hooks。

Apps consume via composables in their own code:

```ts
import { usePreferences } from '@vben/preferences';
import { LAYOUTS } from '@vben/preferences';
```

## 禁止

- Don't add Vue hooks here
- Don't add reactive state
