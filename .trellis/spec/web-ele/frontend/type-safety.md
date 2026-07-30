# @vben/web-ele Type Safety

> 严格模式 TS 通过 @vben/tsconfig/web-app.json.

## 必需模式

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

## 类型导入

Always `import type`:
```ts
import type { RouteRecordRaw } from 'vue-router';
```

## 禁止

- Don't use any
- Don't disable strict mode per-file
- Don't `as` cast to silence errors
- Don't @ts-ignore without comment
