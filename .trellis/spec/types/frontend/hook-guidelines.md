# @vben/types Hook Guidelines

> No composables — types are consumed by `useXxx()` in apps.

## Purpose

`@vben/types` does not define `useXxx()` composables. It is a pure type
namespace. Composables that **use** these types live in `@vben/hooks`
and `@vben-core/composables`. This file documents the contract so
consumers know what types to feed into their hooks.

## Pattern: hook with typed return

```ts
// apps/web-antdv-next/src/views/preferences/preferences-button.vue
import type { MenuRecordRaw } from '@vben/types';
import { storeToRefs } from 'pinia';
import { useAccessStore } from '@vben/stores';

const { accessMenus } = storeToRefs(useAccessStore());
// accessMenus: Ref<MenuRecordRaw[]>

function findMenu(path: string): MenuRecordRaw | undefined {
  return accessMenus.value.find((m) => m.path === path);
}
```

## Pattern: form hook with typed payload

```ts
// apps/web-antdv-next/src/views/authentication/login.vue
import type { Recordable, UserInfo } from '@vben/types';
import { useForm } from '@vben/hooks';

const formApi = useForm<Recordable<any>, UserInfo>({
  onSubmit: async (values) => {
    const userInfo = await authLogin(values);
    return userInfo;
  },
});
```

## Pattern: store action with typed arg

```ts
// apps/web-antdv-next/src/store/auth.ts
import type { Recordable, UserInfo } from '@vben/types';

async function authLogin(
  params: Recordable<any>,
  onSuccess?: () => Promise<void> | void,
): Promise<{ userInfo: null | UserInfo }> {
  // ...
  return { userInfo };
}
```

## Pattern: tab definition with router type

```ts
// packages/@core/base/typings/src/tabs.ts
import type { RouteLocationNormalized } from 'vue-router';
import type { TabDefinition } from '@vben/types';

interface UseTabbarReturn {
  addTab: (tab: TabDefinition) => TabDefinition;
  closeTab: (tab: TabDefinition, router: Router) => Promise<void>;
}
```

## Conventions

- **Hooks declare `useXxx<T1, T2>()`** — generic type params for
  typed payloads.
- **Domain types** come from `@vben/types`; utility helpers
  (`MaybeRef`, `Recordable`, `DeepPartial`) from `@vben-core/typings`.
- **No `any` returns** — declare the return type explicitly.
- **Generic hooks** constrain with `extends object` where possible.
- **No runtime polymorphism** in this package — apps do that.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Composable | `useXxx<T>(...)` | `useForm<TValues, TResponse>(...)` |
| Type param | `T...`, `TResult`, `TPayload` | `TFormValues` |
| Return shape | declared `interface` or `type` | `UseTabbarReturn` |
| Domain type | from `@vben/types` | `UserInfo`, `MenuRecordRaw` |

## Forbidden

- ❌ 不要 add `useXxx()` composables to this package — pure types
- ❌ 不要 use `any` for hook payloads — declare types
- ❌ 不要 define runtime refs in this package — type-only
- ❌ 不要 skip `import type` for `MenuRecordRaw` etc.
- ❌ 不要 put `RouteRecordRaw` augments here without `vue-router` `import type`
- ❌ 不要 overload hooks with union types — use a discriminator
- ❌ 不要 export an interface that mixes runtime + type members
