# @vben/constants Type Safety

> Strict-mode TS, zero runtime concerns (this package is pure types + values).

## Config

`packages/constants/tsconfig.json`:

```json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Library config enables:
- `"strict": true`
- `"noUnusedLocals": true`
- `"noUnusedParameters": true`
- `"noImplicitOverride": true`
- `"verbatimModuleSyntax": true`

## Required Patterns

### 1. Strict-type consts

```ts
// ✅ Good — literal-typed
export const LOGIN_PATH = '/auth/login' as const;

// ✅ Good — string union type
export type LayoutType =
  | 'sidebar-nav'
  | 'mixed-nav'
  | 'header-nav'
  | 'header-sidebar-nav';
```

### 2. Interface declarations

```ts
export interface UserInfo {
  id: string;
  realName: string;
  email?: string;
}
```

### 3. Type alias for unions

```ts
export type AccessToken = null | string;
export type ThemeMode = 'auto' | 'dark' | 'light';
```

## Type Imports

When importing types into other packages, use `import type`:

```ts
import type { UserInfo, LayoutType } from '@vben/constants';
import { LOGIN_PATH, HOME_PATH } from '@vben/constants';  // value 导入不加 type
```

## Typecheck

```bash
pnpm typecheck                       # vue-tsc on whole monorepo
pnpm typecheck --filter @vben/constants  # 单包
```

## Forbidden

- ❌ 不要用 `any`
- ❌ 不要用 `Object` as type — 用 `Record<string, T>` 或明确 interface
- ❌ 不要 disable strict mode per-file
- ❌ 不要用 `as` cast 来 silence errors — refactor 替换
- ❌ 不要 `@ts-ignore` / `@ts-expect-error` 没有 `// why:` comment
- ❌ 不要重复 export 既有 type — 用 re-export from 'src/index.ts'
