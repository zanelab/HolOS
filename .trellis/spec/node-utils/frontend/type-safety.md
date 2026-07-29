# @vben/node-utils Type Safety

> Strict-mode TS, no `any`.

## Config

`tsconfig.json` extends `@vben/tsconfig/node.json`:

```json
{
  "extends": "@vben/tsconfig/node.json"
}
```

Enables `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`.

## Required Patterns

### Explicit input/output types

```ts
// src/hash.ts
export function sha256(input: string | Uint8Array): string {
  // explicit union return — never `any`, never implicit `unknown`
}
```

### Discriminated unions for result types

```ts
// src/git.ts
export type GitResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: Error };

export async function gitRevParse(cwd: string): Promise<GitResult<string>> { ... }
```

### Throw on bad input, return value on success

```ts
export function formatBytes(bytes: number, decimals = 2): string {
  if (!Number.isFinite(bytes)) {
    throw new TypeError(`formatBytes: bytes must be a finite number, got ${bytes}`);
  }
  // ...
}
```

## Forbidden

- ❌ Don't use `any` — use `unknown` and narrow with type guards.
- ❌ Don't use `Function` type as parameter — write the function signature explicitly.
- ❌ Don't use `as` cast to silence errors — refactor to a typed function.
- ❌ Don't return `Promise<any>` — always specify the resolved type.
- ❌ Don't use `require()` — it's a strict-mode ESM-only workspace.
