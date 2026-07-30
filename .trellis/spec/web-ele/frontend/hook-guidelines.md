# web-ele Custom Hooks

> Vue 3 + Pinia + @vben/preferences hooks. Don't write new hooks unless necessary.

## Built-ins (always check first)

| Concern | Hook | Source |
|---|---|---|
| App config | `usePreferences()` | @vben/preferences |
| Pinia stores | `useAccessStore`, `useUserStore`, `useAuthStore` | @vben/stores |
| i18n | `useI18n()` | vue-i18n |
| Router | `useRouter()`, `useRoute()` | vue-router |
| Form | `useVbenForm()` | @vben/common-ui |
| Grid | `useVbenVxeGrid()` | @vben/plugins/vxe-table |
| UI library adapter | 随每个 app 自定义 | this app's adapter |

## When to Write a New Hook

- Used by ≥ 3 views / components
- Returns **reactive state** OR a stable async function
- Non-trivial logic (> 10 lines)

## Convention

- `use-<name>.ts` (kebab-case, `use` prefix)
- Co-located for one-feature hooks; shared under `src/hooks/`

## Example: useAsyncResource

```ts
// src/hooks/use-async-resource.ts
import { ref, shallowRef } from 'vue';

export function useAsyncResource<T>(loader: () => Promise<T>) {
  const data = shallowRef<T>();
  const loading = ref(false);
  const error = ref<unknown>();

  async function refresh() {
    loading.value = true;
    try { data.value = await loader(); }
    catch (e) { error.value = e; }
    finally { loading.value = false; }
  }

  return { data, loading, error, refresh };
}
```

## For element-plus Specific

```ts
// For Naive UI
import { useMessage } from 'naive-ui';
export function useToast() {
  const msg = useMessage();
  return {
    success: (content: string) => msg.success(content),
    error: (content: string) => msg.error(content),
  };
}
```

## Forbidden

- ❌ Don't wrap usePreferences() in another useFoo()
- ❌ Don't put pure business logic in a hook
- ❌ Don't use hooks outside <script setup>
- ❌ Don't make localStorage-wrappers "hooks"
- ❌ Don't create per-flavor mixin — composition API only
