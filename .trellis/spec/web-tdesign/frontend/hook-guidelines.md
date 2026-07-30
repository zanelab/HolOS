# @vben/web-tdesign Custom Hooks

> Compose **existing** hooks before writing a new one.

## 可用的内置函数 (no need to re-implement)

| Concern | Hook | Source |
|---|---|---|
| App config | `usePreferences()` | `@vben/preferences` |
| Pinia stores | `useAccessStore`, `useUserStore`, `useAuthStore` | `@vben/stores` |
| i18n | `useI18n()` | `vue-i18n` |
| Router | `useRouter()`, `useRoute()` | `vue-router` |
| Dark mode | `useDark()` | `@vueuse/core` |
| Throttle / debounce | `useThrottleFn`, `useDebounceFn` | `@vueuse/core` |
| Form state | `useVbenForm()` | `@vben/common-ui` |
| Grid/table | `useVbenVxeGrid()` | `@vben/plugins/vxe-table` |

## 何时 Write a Custom Hook

Write a hook if (and only if):
- It is used by ≥ 3 views / components
- It returns **reactive state** OR a stable async function
- Its logic is **non-trivial** (> 10 lines) and lives in a view's `setup()` script block

## Convention

- File naming: `use-<name>.ts` (kebab-case, starts with `use`)
- Co-located with the view if only used by one feature (`src/views/dashboard/useFoo.ts`)
- Or shared under `src/hooks/use-<name>.ts`

## 示例 (real pattern)

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

Then in a view:

```vue
<script setup>
import { useAsyncResource } from '#/hooks/use-async-resource';
import { fetchUsers } from '#/api';
const { data: users, loading, refresh } = useAsyncResource(fetchUsers);
</script>
```

## 禁止

- ❌ Don't wrap `usePreferences()` in another `useFoo()` — call `usePreferences()` directly.
- ❌ Don't put pure business logic (no state, no async) in a hook — it's a regular helper, goes in `src/utils/`.
- ❌ Don't use hooks outside of `<script setup>` or `<script lang="ts" setup>` — they need a Vue component context.
- ❌ Don't make hooks for "Read X from localStorage" — that's a service, not a hook.
