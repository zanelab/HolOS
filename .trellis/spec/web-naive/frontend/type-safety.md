# web-naive Type Safety

> Strict-mode TS via @vben/tsconfig/web-app.json.

## TS Config

```json
{
  "extends": "@vben/tsconfig/web-app.json"
}
```

启用 strict mode / noUnusedLocals / noUnusedParameters / noImplicitOverride.

## Required Patterns

### Route records

```ts
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/analytics',
    component: () => import('#/views/dashboard/analytics/index.vue'),
    meta: { title: 'Analytics' },
  },
];
```

### API responses

```ts
import { requestClient } from '#/api/request';
export interface UserInfo { id: string; realName: string; email?: string; }
export async function fetchUserInfo() {
  return requestClient.get<UserInfo>('/user/info');
}
```

### Props (Vue 3.4+)

```vue
<script lang="ts" setup>
interface Props { title: string; count?: number; }
const props = withDefaults(defineProps<Props>(), { count: 0 });
</script>
```

## Type Imports

Always `import type`:

```ts
import type { RouteRecordRaw } from 'vue-router';
import type { UserInfo } from '#/api/core/user';
```

## naive-ui Type Patterns

```ts
import type { ButtonProps, SelectProps } from 'naive-ui';

interface ActionProps extends ButtonProps {
  // app-specific extensions
  customAction?: string;
}
```

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter web-naive
```

## Forbidden

- ❌ Don't use `any`
- ❌ Don't disable strict mode per-file
- ❌ Don't use `as` cast to silence errors — refactor to typed function
- ❌ Don't `@ts-ignore` without `// why:`
- ❌ Don't override `skipLibCheck: true` per-file
- ❌ Don't bypass strict mode for naive-ui libs (forward issues to maintainer)
