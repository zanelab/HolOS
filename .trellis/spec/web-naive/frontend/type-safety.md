# @vben/web-naive Type Safety

> Strict-mode TS via @vben/tsconfig/web-app.json.

## Required Patterns

### Route records
```ts
import type { RouteRecordRaw } from 'vue-router';
const routes: RouteRecordRaw[] = [...];
```

### API responses
```ts
import { requestClient } from '#/api/request';
export async function fetchFoo() {
  return requestClient.get<FooResponse>('/foo');
}
```

### Props
```vue
<script setup lang="ts">
interface Props { title: string; count?: number; }
const props = withDefaults(defineProps<Props>(), { count: 0 });
</script>
```

## Type Imports

Always `import type`:
```ts
import type { RouteRecordRaw } from 'vue-router';
```

## Forbidden

- Don't use any
- Don't disable strict mode per-file
- Don't `as` cast to silence errors
- Don't @ts-ignore without comment
