# @vben/types Quality Guidelines

> Type-only. Tree-shake friendly. Strict mode enforced.

## Purpose

`@vben/types` is the strict type backbone. The quality bar is: every
export is named, every type is reused, no runtime footprint, and
circular imports are impossible by construction.

## TS file style

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

- **2-space indent**
- **Single quotes**
- **No semicolons**
- **Trailing newline**
- **`import type`** for type-only imports
- **`export type { ... }`** for re-exports (no `export *` of types — explicit)
- **`interface` for shape, `type` for unions/aliases**

## Upstream d.ts style

```ts
// packages/@core/base/typings/src/basic.d.ts (real)
interface BasicOption {
  label: string;
  value: string;
}

type SelectOption = BasicOption;
type TabOption = BasicOption;

interface BasicUserInfo {
  avatar: string;
  realName: string;
  roles?: string[];
  userId: string;
  username: string;
}

type ClassType =
  | Array<ClassType>
  | boolean
  | null
  | object
  | string
  | undefined;

export type { BasicOption, BasicUserInfo, ClassType, SelectOption, TabOption };
```

- **No `import` from runtime** — `.d.ts` files only carry types.
- **Trailing comma** in multi-line `export type { ... }`.

## Conventions

- **Single barrel** at `src/index.ts` — re-exports only.
- **Type-only exports** — never `export const X = ...` here.
- **No defaults** — `export type *` is the only valid bulk export.
- **Extend upstream** — don't re-declare `BasicUserInfo`.
- **No `any`** — `unknown` if shape is unknown.
- **No `as` casts** — types should be correct, not forced.
- **`import type`** for everything.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Interface | `PascalCase` | `UserInfo`, `BasicUserInfo` |
| Type alias | `PascalCase` | `Recordable`, `Nullable` |
| Generic param | `T...` | `TFormValues`, `TPayload` |
| File | `camelCase.ts` | `user.ts`, `basic.d.ts` |

## Linting & pre-commit

- ESLint flat config
- OxLint
- OxFmt
- `pnpm typecheck` includes `@vben/types`
- `tsc --noEmit` strict + `verbatimModuleSyntax`

## Forbidden

- ❌ 不要 export a runtime value — type-only
- ❌ 不要 add `default` exports — break tree-shaking
- ❌ 不要 `as any` — fix the type
- ❌ 不要 redefine upstream types — extend them
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 put `export *` from a runtime module — explicit named re-exports
- ❌ 不要 skip `import type` for cross-package type imports
