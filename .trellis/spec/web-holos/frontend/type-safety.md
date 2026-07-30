# Web-Holos Type Safety

> Strict-mode TS for the customised Vue 3 + TDesign-Vue-Next app.

## TS Config

```json
{
  "extends": "@vben/tsconfig/web-app.json"
}
```

Wbn web app config enables:
- `"strict": true`
- `"noUnusedLocals": true`
- `"noUnusedParameters": true`
- `"noImplicitOverride": true`
- `"exactOptionalPropertyTypes": true`

## Required Patterns

### 1. Route records

```ts
// apps/web-holos/src/router/routes/core.ts (real)
import type { RouteRecordRaw } from 'vue-router';
import { LOGIN_PATH } from '@vben/constants';
import { preferences } from '@vben/preferences';

const coreRoutes: RouteRecordRaw[] = [
  {
    meta: {
      icon: 'lucide:home',
      title: '首页',
    },
    name: 'Root',
    path: '/',
    redirect: () => preferences.app.defaultHomePath,
  },
  {
    name: 'HolOSHome',
    path: '/home',
    component: () => import('#/views/home/index.vue'),
    meta: { ignoreAccess: true },
  },
];
```

### 2. API responses

```ts
// apps/web-holos/src/api/core/auth.ts
import { requestClient } from '#/api/request';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: 'Bearer';
}

export async function login(body: LoginRequest) {
  return requestClient.post<LoginResponse>('/auth/login', body);
}
```

### 3. Props (Vue 3.4+ Generic Declaration)

```vue
<script lang="ts" setup>
interface Props {
  title: string;
  count?: number;
  items?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => [] as string[],
});
</script>
```

### 4. TDesign Component Props

```vue
<script lang="ts" setup>
import type { TabsProps } from 'tdesign-vue-next';

const tabsProps = ref<TabsProps>({
  value: 'home',
  list: [
    { label: '首页', value: 'home' },
    { label: '关于', value: 'about' },
  ],
});
</script>

<template>
  <TTabs v-bind="tabsProps" />
</template>
```

## Type Imports

Always **explicit `import type`**:

```ts
import type { RouteRecordRaw } from 'vue-router';
import type { UserInfo } from '#/api/core/user';
import type { TabsProps, TableProps } from 'tdesign-vue-next';
```

`verbatimModuleSyntax` 在 web-app.json 启用 — required explicit `type` 关键字。

## HolOS-Specific Types

```ts
// apps/web-holos/src/types/holos.d.ts
declare module '*.vue' {
  import type { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
```

## Typecheck

```bash
pnpm typecheck                  # 全 workspace
pnpm typecheck --filter @vben/web-holos  # 单 app
```

## Forbidden

- ❌ Don't use `any`
- ❌ Don't disable strict mode per-file via `// @ts-nocheck`
- ❌ Don't use `as` cast to silence errors — refactor to typed function
- ❌ Don't `@ts-ignore` without `// why:` comment
- ❌ Don't override `skipLibCheck: true` per-file(虽然 base 启用)
- ❌ Don't import 'tdesign-vue-next' types without `import type` prefix
- ❌ Don't mutate props in Vue templates (one-way reactivity)
- ❌ Don't skip Pinia state typing (`useAuthStore()` returns `Store<T>` typed)
