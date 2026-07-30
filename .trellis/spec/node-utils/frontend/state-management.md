# @vben/node-utils: State / Caching Patterns

> 本包 **stateless**. No caches, no module-level state.

## Implications

- Each function call is independent (no hidden cache).
- Callers (scripts / pipelines) own any caching they need.

## 模式: externalize cache at caller site

```ts
// .trellis/scripts/with-cache.ts
import { hash } from '@vben/node-utils';

const cache = new Map<string, string>();

export function cachedHash(content: Uint8Array): string {
  const key = content.toString(); // big string → fine for short content
  if (!cache.has(key)) cache.set(key, hash(content));
  return cache.get(key)!;
}
```

This is **explicit**, **testable**, and stays out of `@vben/node-utils`.

## 原因 node-utils stays stateless

- **Embedding**: Trellis scripts run multiple times per session; state from a previous run must not leak.
- **Concurrency**: when parallelizing across worktree, state corruption is avoided by being stateless.
- **Testing**: each test runs deterministically — no hidden cache invalidation logic to fight.

## 禁止

- ❌ Don't add module-level mutable state to `@vben/node-utils`.
- ❌ Don't make any helper "remember" inputs across calls.
- ❌ Don't introduce singletons (e.g. a single `Spinners` instance) — let callers manage state.
