# @vben/constants Quality Guidelines

> Strict-mode TS, zero runtime deps.

## 代码风格

```ts
// 一致风格 (实际 vben v5.7.0 风格)
export const LOGIN_PATH = '/auth/login' as const;

export interface UserInfo {
  id: string;
  realName: string;
  email?: string;
}

export type LayoutType = 'sidebar-nav' | 'header-nav' | /* ... */;
```

### Indentation / Quote / Punctuation
- **4-space** TS indent (not 2)
- **Single quotes** for strings
- **No trailing comma** (each line is clean)
- **Trailing newline** at end of file
- **No semicolons** in TS (依赖 OxFmt 提交时 auto-insert)

### Naming

| Thing | Convention | Example |
|---|---|---|
| Constant | UPPER_SNAKE_CASE | LOGIN_PATH, HOME_PATH, APP_NAME_DEFAULT |
| Type | PascalCase | UserInfo, LayoutType, AccessToken |
| Interface | PascalCase + 'I' prefix optional | OR 不带 prefix 是 v5.7.0 风格 |

## Patterns

### Const declaration

```ts
export const LOGIN_PATH = '/auth/login';
//                  ^ 实际 char 型值 string
```

### Type union

```ts
// 把允许的 layout mode 用 string literal union 表示
export type LayoutType =
  | 'sidebar-nav'
  | 'mixed-nav'
  | 'header-nav'
  | /* ... */;
```

### Interface

```ts
export interface UserInfo {
  id: string;
  realName: string;
  email?: string;       // optional fields 用 ?
  avatar?: string;
  homePath: string;     // required
}
```

## Tests

不需要 — types-only / const-only package 编译时已被 TypeScript-checked。

## Pre-commit Hooks

- OxLint (fast linter)
- OxFmt (formatter on commit)
- ESLint flat config (rules OxLint misses)
- commitlint (`feat():` / `fix():` / `chore():`)

## Forbidden

- ❌ 不要引入 npm 依赖 — 这是 leaf package
- ❌ 不要加 IO functions (network / fs / async-await)
- ❌ 不要把 functions 包进 classes / namespaces
- ❌ 不要 mutate exported consts (`const` 已天然 immutable)
- ❌ 不要加 'use strict' — strict mode 在 tsconfig 启用
- ❌ 不要 commit `.env` 或 secret
