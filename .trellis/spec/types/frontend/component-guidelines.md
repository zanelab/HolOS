# @vben/types Component Guidelines

> No Vue components — `interface` and `type` declarations only.

## Purpose

`@vben/types` ships no Vue SFCs. "Components" here are **type
declarations** that Vue components consume. They are the contract
between the data layer (API, stores) and the visual layer (templates).

## Pattern: domain interface

```ts
// packages/types/src/user.ts (verified)
import type { BasicUserInfo } from '@vben-core/typings';

interface UserInfo extends BasicUserInfo {
  desc: string;
  homePath: string;
  token: string;
}

export type { UserInfo };
```

## Pattern: menu record

```ts
// packages/@core/base/typings/src/menu-record.ts (real)
import type { Component } from 'vue';
import type { RouteRecordRaw } from 'vue-router';
import type { Recordable } from './helper';

interface MenuRecordBadgeRaw {
  badge?: string;
  badgeType?: 'dot' | 'normal';
  badgeVariants?: 'destructive' | 'primary' | string;
}

interface MenuRecordRaw extends MenuRecordBadgeRaw {
  activeIcon?: string;
  children?: MenuRecordRaw[];
  disabled?: boolean;
  icon?: Component | string;
  name: string;
  order?: number;
  path: string;
  query?: Recordable<any>;
  show?: boolean;
}
```

## Pattern: tab definition

```ts
// packages/@core/base/typings/src/tabs.ts
import type { RouteLocationNormalized } from 'vue-router';

interface TabDefinition extends RouteLocationNormalized {
  key?: string;
}
```

## How components consume

```vue
<!-- apps/web-antdv-next/src/store/auth.ts (real) -->
<script setup lang="ts">
import type { Recordable, UserInfo } from '@vben/types';

const userInfo: Ref<null | UserInfo> = ref(null);

async function authLogin(params: Recordable<any>) {
  // ...
}
</script>
```

## Real component prop typing

```ts
// apps/web-antdv-next/src/components/Page.ts (real pattern)
import type { MenuRecordRaw } from '@vben/types';

const props = defineProps<{
  menus: MenuRecordRaw[];
  activePath?: string;
}>();
```

## Conventions

- **Every component prop** is typed via `defineProps<{ ... }>()` (script
  setup) — no runtime `defineProps({})` object form.
- **Domain types** come from `@vben/types` — components don't re-declare
  `UserInfo`/`MenuRecordRaw`.
- **Generic components** accept `<T>` for collection items where the
  item shape is open.
- **`emits` typing** uses `defineEmits<{ (e: 'change', v: string): void }>()`.
- **No `any` props** — declare the structure.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Component prop interface | inline `defineProps<{ ... }>()` | — |
| Domain type | `UserInfo`, `MenuRecordRaw` | — |
| Event payload | inline `defineEmits<{ ... }>()` | — |
| Slot scope | `defineSlots<{ default?: (props: Foo) => any }>()` | — |

## Forbidden

- ❌ 不要 add `defineComponent({...})` definitions here — runtime code
- ❌ 不要 re-declare `UserInfo` in app code — import from `@vben/types`
- ❌ 不要 use `any` in component prop types — declare the structure
- ❌ 不要 define template-only structural types here — inline them
- ❌ 不要 import Vue runtime inside `.d.ts` files unless `import type`
- ❌ 不要 put business types here that only one app uses — local type file
- ❌ 不要 skip slot typings when slots take structured props
