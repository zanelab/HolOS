# @vben/types State Management

> No state. Types are passive contracts.

## Purpose

`@vben/types` defines interfaces that **state** elsewhere (stores,
preferences, API responses) conforms to. This package has no runtime
state, no `ref`/`reactive`, no Pinia. Reactive state lives in
`@vben/stores` and `@vben/preferences`; static defaults live in
`@vben-core/typings` and `@vben-core/preferences`.

## Type contracts

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

```ts
// packages/@core/base/typings/src/basic.d.ts
interface BasicUserInfo {
  avatar: string;
  realName: string;
  roles?: string[];
  userId: string;
  username: string;
}
```

## Where the state lives

| State | Type | Owned by |
|---|---|---|
| `UserInfo` | `interface` | `@vben/types` (definition) |
| `useUserStore` | Pinia store | `@vben/stores` (instance) |
| `preferences.user` | `reactive` | `@vben/preferences` (instance) |
| API response | `UserInfo` | backend-mock (data) |

## Reactive store conformed to type

```ts
// packages/stores/src/modules/user.ts (real)
interface AccessState {
  userInfo: BasicUserInfo | null;
  userRoles: string[];
}

export const useUserStore = defineStore('core-user', {
  state: (): AccessState => ({
    userInfo: null,
    userRoles: [],
  }),
  actions: {
    setUserInfo(userInfo: BasicUserInfo | null) {
      this.userInfo = userInfo;
      const roles = userInfo?.roles ?? [];
      this.setUserRoles(roles);
    },
  },
});
```

The store's state conforms to `AccessState` (`userInfo` is
`BasicUserInfo | null`), and `@vben/types` extends `BasicUserInfo` to
add app-specific fields.

## State surface map

| Type | Used by |
|---|---|
| `UserInfo` | `auth.ts`, `user.ts`, `login-api.ts` |
| `MenuRecordRaw` | `access.ts`, menu rendering, route generation |
| `TabDefinition` | `tabbar.ts`, multi-tab views |
| `Recordable<T>` | API client, form payloads |
| `DeepPartial<T>` | `defineOverridesPreferences` |

## Conventions

- **Types are passive** — no `ref`/`reactive` here.
- **State is owned by stores/preferences** — `useUserStore`,
  `preferences.user`.
- **API responses** declare `UserInfo | null` — explicit nullability.
- **Discriminated unions** for state with variants (e.g., `loginExpired : boolean`).
- **Type-only imports** — `import type { ... }`.

## Forbidden

- ❌ 不要 create a Pinia store in this package — type-only
- ❌ 不要 add `ref`/`reactive` to a type file — runtime code
- ❌ 不要 hold default values that change at runtime — use `defaultPreferences`
- ❌ 不要 redefine `UserInfo` in app code — import from `@vben/types`
- ❌ 不要 put `as const` arrays in this package — types-only
- ❌ 不要 bind state to a `.ts` file with a default export — names only
- ❌ 不要 add `WeakMap` / `Set` shapes — those are runtime concerns
