# @vben/node-utils Type Safety

> 严格模式 TS, no `any`.

## 配置

`tsconfig.json` extends `@vben/tsconfig/node.json`:

```json
{
  "extends": "@vben/tsconfig/node.json"
}
```

Enables `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`.

## 必需模式

### 显示的输入/输出类型

```ts
// src/hash.ts
export function sha256(input: string | Uint8Array): string {
  // explicit union return — never `any`, never implicit `unknown`
}
```

### 用可辨识的枚举表示结果类型

```ts
// src/git.ts
export type GitResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: Error };

export async function gitRevParse(cwd: string): Promise<GitResult<string>> { ... }
```

### 输入非法时抛出，成功时返回值

```ts
export function formatBytes(bytes: number, decimals = 2): string {
  if (!Number.isFinite(bytes)) {
    throw new TypeError(`formatBytes: bytes must be a finite number, got ${bytes}`);
  }
  // ...
}
```

## 禁止

- ❌ Don't use `any` — use `unknown` and narrow with type guards.
- ❌ Don't use `Function` type as parameter — write the function signature explicitly.
- ❌ Don't use `as` cast to silence errors — refactor to a typed function.
- ❌ Don't return `Promise<any>` — always specify the resolved type.
- ❌ Don't use `require()` — it's a strict-mode ESM-only workspace.
