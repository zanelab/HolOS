# @vben/types Directory Structure

> Real layout for `packages/types/`. Source verified 2026-07-30.

## Purpose

`@vben/types` is the workspace's **app-level type package**. It owns
shared interfaces used across web-* apps (e.g., `UserInfo`) and
re-exports the deeper `@vben-core/typings` helpers (`DeepPartial`,
`Recordable`, `MenuRecordRaw`, `TabDefinition`, etc.). It is a pure
type-only package — no runtime values, no JS.

## 目录树 (verified from `packages/types/`)

```
@vben/types/                        # workspace: packages/types/
├── package.json                    # name "@vben/types" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
└── src/
    ├── index.ts                    # public barrel
    └── user.ts                     # UserInfo extends BasicUserInfo
```

## Re-exported upstream

The public barrel re-exports `@vben-core/typings` so apps can import
deep helpers without learning the layered package layout:

```ts
// packages/types/src/index.ts
export type * from './user';
export type * from '@vben-core/typings';
```

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

## Upstream surface (`@vben-core/typings`)

| File | Exports |
|---|---|
| `basic.d.ts` | `BasicOption`, `BasicUserInfo`, `ClassType`, `SelectOption`, `TabOption` |
| `menu-record.ts` | `ExRouteRecordRaw`, `MenuRecordBadgeRaw`, `MenuRecordRaw` |
| `tabs.ts` | `TabDefinition` |
| `helper.d.ts` | `DeepPartial`, `DeepReadonly`, `Recordable`, `Nullable`, `MaybeComputedRef`, `Merge`, `MergeAll`, etc. |
| `app.d.ts` | `Application Configuration` types |
| `vue-router.d.ts` | `vue-router` augmentations |

## Conventions

- **Single barrel** at `src/index.ts` — re-exports only.
- **Type-only** — all exports are `type` or `interface`.
- **Tree-shake friendly** — each export is named.
- **No runtime code** — `tsconfig.json` would error on a `lib` mismatch.
- **No `default`** — every export is a named export to keep typing
  transparent.
- **Extends upstream** — `UserInfo` extends `BasicUserInfo` to add
  app-specific fields.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Interface | `PascalCase` | `UserInfo`, `BasicUserInfo` |
| Type alias | `PascalCase` | `Recordable`, `Nullable` |
| File | `camelCase.ts` or `<scope>.d.ts` | `user.ts`, `basic.d.ts` |
| Barrel | `src/index.ts` | — |

## Forbidden

- ❌ 不要 add runtime values — type-only
- ❌ 不要 add `default` exports — they break tree-shaking
- ❌ 不要 redefine upstream types — extend them
- ❌ 不要 introduce Vue `defineComponent` opts here — runtime concern
- ❌ 不要 skip `import type` — strict mode + `verbatimModuleSyntax`
- ❌ 不要 put business-scoped types here — use `@vben-core/typings`
- ❌ 不要 add `as` casts here — types should be correct, not forced
