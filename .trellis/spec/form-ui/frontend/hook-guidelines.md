# form-ui Custom Hooks

> **PLACEHOLDER DOCS** - 本包 does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. 替换这些文件 real content when package 添加后.

## 预期约定

- For Vue apps: composables go in src/composables/
- Co-located hooks in src/views/<feature>/ for one-feature usage
- Shared hooks in src/hooks/
- For libs: package itself has no Vue hooks (consumed via Vue apps)

## 示例 (synthetic)

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

## 内置函数（始终优先检查）

| Concern | Hook | Source |
|---|---|---|
| App config | usePreferences() | @vben/preferences |
| Pinia | useAccessStore / useUserStore / useAuthStore | @vben/stores |
| i18n | useI18n() | vue-i18n |

## 禁止

- 不要 implement against this phantom package before it exists
- 不要 wrap usePreferences() in another composable
- 不要 put pure business logic in a hook (use src/utils/ instead)
