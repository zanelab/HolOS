# layouts — PLACEHOLDER SPEC

**Expected package:** `@vben/layouts` — Top-level layouts — `BasicLayout`, `AuthenticationLayout`, `IFrameView`, `BlankLayout`. Compose layout-ui + menu-ui + tabs-ui + common-ui.

> ⚠️ **PLACEHOLDER DOCS** — This package does **not** exist in the current
> workspace. The structure, conventions, and code examples below are
> best-guess projections based on the upstream `vben v5.7.0` monorepo
> (`vbenjs/vben-admin-monorepo`) and the role this package plays
> in a real vben app. **Replace this file with real content when (and
> only when) the corresponding `packages/layouts/`
> directory lands upstream.**

Do **not** implement against this placeholder — code that imports from
`@vben/layouts` will fail to typecheck.
## tsconfig

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
- `"noFallthroughCasesInSwitch": true`

## Type patterns

### 1. Generic utility types (core of `@vben/layouts` for typings role)

```ts
export type Nullable<T> = T | null;
export type Recordable<T = unknown> = Record<string, T>;
export type AnyFunction = (...args: any[]) => any;
export type AnyObject = Record<string, any>;
export type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
export type ElementOf<T extends readonly unknown[]> = T[number];
export type PromiseFn<T = void> = () => Promise<T>;
```

### 2. Discriminated unions

```ts
export type AccessResult =
  | { kind: 'allow'; reason?: string }
  | { kind: 'deny'; reason: string }
  | { kind: 'pending' };
```

### 3. Component prop types

```vue
<script setup lang="ts">
interface Props {
  open: boolean;
  title: string;
  onOk?: () => Promise<void> | void;
}
const props = withDefaults(defineProps<Props>(), { open: false });
const emit = defineEmits<{ (e: 'update:open', v: boolean): void }>();
</script>
```

### 4. `MaybeRefOrGetter` for composable inputs

```ts
import type { MaybeRefOrGetter } from 'vue';
export function useX(target: MaybeRefOrGetter<HTMLElement | null>) {
  // ...
}
```

### 5. `import type` discipline

```ts
// ✅ type-only import — erased at compile
import type { RouteRecordRaw, Router } from 'vue-router';
import { createRouter } from 'vue-router';
```

## Typecheck

```bash
pnpm typecheck                            # whole monorepo
pnpm typecheck --filter @vben/layouts       # this package only
```

## Forbidden

- ❌ Don't use `any` — use `unknown` + narrowing, or a proper type.
- ❌ Don't use `Object` as a type — use `Record<string, T>` or an
  interface.
- ❌ Don't disable strict mode per-file.
- ❌ Don't use `as` casts to silence errors — refactor.
- ❌ Don't use `@ts-ignore` / `@ts-expect-error` without a `// why:`
  comment on the line above.
- ❌ Don't re-export types from `node_modules` directly — wrap with a
  `@vben/layouts`-scoped alias.
- ❌ Don't import types using `import { type X }` and value in one
  statement — split into two `import type` and value `import`.
