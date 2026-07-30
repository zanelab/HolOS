# plugins Custom Hooks

> **PLACEHOLDER DOCS** - This package does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. Replace these files with real content when the package is added.

## Expected Conventions

- For Vue apps: composables go in src/composables/
- Co-located hooks in src/views/<feature>/ for one-feature usage
- Shared hooks in src/hooks/
- For libs: package itself has no Vue hooks (consumed via Vue apps)

## Example (synthetic)

```ts
// src/composables/use-x-resource.ts
import { ref, shallowRef } from "vue";

export function useXResource(loader: () => Promise<XData>) {
  const data = shallowRef<XData>();
  const loading = ref(false);
  async function refresh() {
    loading.value = true;
    try { data.value = await loader(); }
    finally { loading.value = false; }
  }
  return { data, loading, refresh };
}
```

## Built-ins (always check first)

| Concern | Hook | Source |
|---|---|---|
| App config | usePreferences() | @vben/preferences |
| Pinia | useAccessStore / useUserStore / useAuthStore | @vben/stores |
| i18n | useI18n() | vue-i18n |

## Forbidden

- Do not implement against this phantom package before it exists
- Do not wrap usePreferences() in another composable
- Do not put pure business logic in a hook (use src/utils/ instead)
