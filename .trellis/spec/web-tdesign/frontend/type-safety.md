# @vben/web-tdesign Type Safety

> 严格模式 TS is **non-negotiable** 在本项目中。

## 配置

`tsconfig.json` extends `@vben/tsconfig/web-app.json`:

```json
{
  "extends": "@vben/tsconfig/web-app.json"
}
```

The base config enables:
- `"strict": true` (all strict flags)
- `"noUnusedLocals": true`
- `"noUnusedParameters": true`
- `"noImplicitOverride": true`
- `"noFallthroughCasesInSwitch": true`

## 必需模式

### Typing route records

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

### Typing API responses

```ts
// src/api/core/user.ts
import { requestClient } from '#/api/request';

export interface UserInfo {
  id: string;
  realName: string;
  email: string;
}

export async function fetchUserInfo() {
  return requestClient.get<UserInfo>('/user/info');
}
```

### Typing props

```vue
<script lang="ts" setup>
interface Props {
  title: string;
  count?: number;
}
const props = withDefaults(defineProps<Props>(), {
  count: 0,
});
</script>
```

## 类型导入

Always use **`import type`** for types:

```ts
import type { RouteRecordRaw } from 'vue-router';
import type { UserInfo } from '#/api/core/user';
```

## Typecheck Commands

```bash
pnpm typecheck                       # local
pnpm typecheck --filter @vben/web-tdesign  # turbo-filtered
```

## 禁止

- ❌ Don't use `any` (use `unknown` + narrowing instead).
- ❌ Don't disable strict mode in subdirs with `// @ts-strict-off` — fix the type, don't fight the compiler.
- ❌ Don't use `as` cast to silence errors — refactor to a typed function.
- ❌ Don't `// @ts-ignore` without a `// why:` comment.
- ❌ Don't enable `skipLibCheck: true` per-file (it's set globally for performance — don't override locally).
