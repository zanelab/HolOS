# @vben/node-utils: State / Caching Patterns

> 本包 **stateless**. No caches, no module-level state.

## 含义

- 每次函数调用独立（无隐藏缓存）。
- 调用方（脚本 / 管线）自行管理所需缓存。

## 模式：在调用方外部化缓存

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

## 为什么 node-utils 保持无状态

- **嵌入**：Trellis 脚本每会话运行多次；上次运行的状态不能泄漏。
- **并发**：在 worktree 上并行时，以无状态避免状态破坏。
- **测试**：每个测试确定性运行 — 无隐藏缓存失效逻辑需要争扫。

## 禁止

- ❌ Don't add module-level mutable state to `@vben/node-utils`.
- ❌ 不要让任何辅助函数跨调用"记住"输入。
- ❌ Don't introduce singletons (e.g. a single `Spinners` instance) — let callers manage state.
