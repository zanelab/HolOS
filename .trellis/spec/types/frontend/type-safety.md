# @vben/types Type Safety

> Strict mode end-to-end. Generics on `Recordable<T>`, `DeepPartial<T>`, etc.

## Purpose

`@vben/types` is the **strict-mode showcase** of the workspace. Every
type is compile-time-checked, every helper has a deterministic shape,
and `import type` is mandatory. The package has no runtime surface —
the strictness is the product.

## Re-export barrel

```ts
// packages/types/src/index.ts
export type * from './user';
export type * from '@vben-core/typings';
```

`export type *` is the bulk re-export pattern that survives
`verbatimModuleSyntax` — it re-exports types only, no runtime values.

## Generic helpers (verified)

```ts
// packages/@core/base/typings/src/helper.d.ts
type Recordable<T> = Record<string, T>;

interface ReadonlyRecordable<T = any> {
  readonly [key: string]: T;
}

type DeepPartial<T, D extends number = 10, C extends unknown[] = []> =
  C['length'] extends D
    ? T
    : T extends object
      ? { [P in keyof T]?: DeepPartial<T[P], D, Increment<C>> }
      : T;

type DeepReadonly<T, D extends number = 10, C extends unknown[] = []> =
  C['length'] extends D
    ? T
    : T extends object
      ? { readonly [P in keyof T]: DeepReadonly<T[P], D, Increment<C>> }
      : T;

type Nullable<T> = null | T;
type NonNullable<T> = T extends null | undefined ? never : T;
type MaybePromise<T> = Promise<T> | T;
type MaybeComputedRef<T> = MaybeReadonlyRef<T> | MaybeRef<T>;
type Merge<O extends object, T extends object> = {
  [K in keyof O | keyof T]: K extends keyof T
    ? T[K]
    : K extends keyof O
      ? O[K]
      : never;
};
```

## Use in stores

```ts
// packages/stores/src/modules/user.ts (real)
interface BasicUserInfo {
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
  state: (): AccessState => ({ userInfo: null, userRoles: [] }),
});
```

## Use in API client

```ts
// apps/web-antdv-next/src/api/core/user.ts (real)
import type { Recordable, UserInfo } from '@vben/types';

export async function getUserInfoApi(): Promise<UserInfo> {
  return request.get<UserInfo>('/user/info');
}

export async function loginApi(
  params: Recordable<any>,
): Promise<{ accessToken: string }> {
  return request.post('/auth/login', params);
}
```

## Strict-mode patterns

### 1. Discriminated union for state

```ts
// ✅ Good — discriminated
type LoginState =
  | { status: 'idle' }
  | { status: 'pending' }
  | { status: 'success'; user: UserInfo }
  | { status: 'error'; error: string };

// ❌ Bad — open shape
type LoginState = {
  status: string;
  user?: UserInfo;
  error?: string;
};
```

### 2. Const-asserted literals

```ts
// ✅ Good — narrow literal
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = typeof ROLES[number];

// ❌ Bad — string
type Role = string;
```

### 3. Readonly with `readonly` keyword

```ts
// ✅ Good
interface ReadonlyRecordable<T = any> {
  readonly [key: string]: T;
}

// ❌ Bad — mutable
interface ReadonlyRecordable<T = any> {
  [key: string]: T;
}
```

## TS config

```json
// packages/types/tsconfig.json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` + `noUnusedLocals`.

## Conventions

- **`export type *`** for bulk re-export — survives `verbatimModuleSyntax`.
- **`import type`** for cross-package imports.
- **Generic defaults** — `Recordable<T>`, `DeepPartial<T, D = 10>`.
- **`null | undefined`** explicit at boundary types.
- **No `any`** — `unknown` for opaque values.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/types
```

## Forbidden

- ❌ 不要 use `any` — `unknown` if shape is unknown
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 `as` casts to silence type errors — refactor
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 `export *` from runtime modules — `export type *` only
- ❌ 不要 add `default` exports — break tree-shaking
- ❌ 不要 re-declare `BasicUserInfo` — extend it
- ❌ 不要 mutate `Recordable<T>` shape — should be `ReadonlyRecordable<T>`
- ❌ 不要 overload types with rest `...args: any[]` — declare each param
