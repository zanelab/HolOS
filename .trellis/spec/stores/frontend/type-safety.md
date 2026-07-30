# @vben/stores Type Safety

> Every store is fully typed. Persistence is opt-in via `pick: [...]`.

## Purpose

`@vben/stores` is the strict-mode Pinia layer. State interfaces are colocated
with the store, actions are typed by their declared argument lists, and
`persist.pick` is the only way to declare what survives reload.

## State interface pattern

```ts
// packages/stores/src/modules/user.ts (verified)
interface BasicUserInfo {
  [key: string]: any;
  avatar: string;
  realName: string;
  roles?: string[];
  userId: string;
  username: string;
}

interface AccessState {
  userInfo: BasicUserInfo | null;
  userRoles: string[];
}

export const useUserStore = defineStore('core-user', {
  actions: {
    setUserInfo(userInfo: BasicUserInfo | null) {
      this.userInfo = userInfo;
      const roles = userInfo?.roles ?? [];
      this.setUserRoles(roles);
    },
    setUserRoles(roles: string[]) {
      this.userRoles = roles;
    },
  },
  state: (): AccessState => ({
    userInfo: null,
    userRoles: [],
  }),
});
```

## Action typing

```ts
// packages/stores/src/modules/access.ts (real)
actions: {
  setAccessToken(token: AccessToken) { this.accessToken = token; },
  setAccessCodes(codes: string[]) { this.accessCodes = codes; },
  getMenuByPath(path: string): MenuRecordRaw | undefined {
    // tree walk
  },
  lockScreen(password: string) { /* ... */ },
  unlockScreen(): void { /* ... */ },
}
```

`AccessToken = null | string` keeps the type explicit.

## Setup-style typing

```ts
// packages/stores/src/modules/timezone.ts (real)
const useTimezoneStore = defineStore(
  'core-timezone',
  () => {
    const timezoneRef = ref(getCurrentTimezone());
    async function setTimezone(timezone: string) {
      timezoneRef.value = timezone;
    }
    return { setTimezone, timezone: timezoneRef };
  },
  { persist: { pick: ['timezone'] } },
);
```

## Pinia + Vue inference

`storeToRefs` infers the same types as the store — no need to declare a
separate type:

```ts
// component
const { accessToken, accessCodes } = storeToRefs(useAccessStore());
// accessToken: Ref<null | string>
// accessCodes: Ref<string[]>
```

## Persistence type contracts

```ts
persist: {
  pick: ['accessToken', 'refreshToken', 'accessCodes', 'isLockScreen', 'lockScreenPassword'],
}
```

`pick` is `string[]` and Pinia asserts the keys exist on the state at
compile-time when using `pinia-plugin-persistedstate` strict variant.

## Conventions

- **`interface` naming** — `<Scope>State` (`AccessState`, `TabbarState`).
- **`type` aliases** for unions — `AccessToken = null | string`.
- **`import type`** for types only.
- **`defineStore` with string id** — devtools-friendly.
- **No `any`** in state shape — extend the interface.

## TS config

```json
// packages/stores/tsconfig.json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` + `noUnusedLocals`.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/stores
```

## Forbidden

- ❌ 不要 use `any` for state fields — typed interfaces only
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 `as` casts to silence store action arg errors
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 pick persistence fields whose schema isn't stable across versions
- ❌ 不要 return `Promise<void>` from getters — actions only
- ❌ 不要 use `[key: string]: any` in interfaces — declare the keys
- ❌ 不要 skip HMR contract — `acceptHMRUpdate` is mandatory
