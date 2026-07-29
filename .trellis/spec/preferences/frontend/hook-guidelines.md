# @vben/preferences: No Hooks

> Pure constants / types package. No Vue hooks.

Apps consume via composables in their own code:

```ts
import { usePreferences } from '@vben/preferences';
import { LAYOUTS } from '@vben/preferences';
```

## Forbidden

- Don't add Vue hooks here
- Don't add reactive state
