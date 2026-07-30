# @vben/icons: No Hooks

> Icon components render-only.

If dynamic switching needed, wrap outside 本包:

```ts
import { usePreferences } from '@vben/preferences';
import { computed } from 'vue';
export function useThemeIcon() {
  const p = usePreferences();
  return computed(() => p.theme.mode === 'dark' ? 'lucide:moon' : 'lucide:sun');
}
```

## 禁止

- Don't add Vue hooks here
