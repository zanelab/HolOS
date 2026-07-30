# @vben/node-utils "Component" Style — Function Helpers

> 本包 doesn't ship Vue components. Its "components" are **pure functions**.

## 模式: Single-export function helpers

Each file in `src/` exports **one or a few related functions**, named exported individually for tree-shaking:

```ts
// src/formatter.ts
export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${sizes[i]}`;
}

export function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60_000) return `${(ms / 1000).toFixed(1)}s`;
  return `${Math.floor(ms / 60_000)}m ${Math.floor((ms % 60_000) / 1000)}s`;
}
```

## 用法 from a downstream app

```ts
import { formatBytes, formatDuration } from '@vben/node-utils';

console.log(formatBytes(1024 * 1024));       // "1 MB"
console.log(formatDuration(123456));        // "2m 3s"
```

## 禁止

- ❌ Don't bundle functions into a class or namespaced object (loses tree-shaking).
- ❌ Don't import Node built-ins at top-level unless necessary — keep imports lean.
- ❌ Don't add async variants of pure sync helpers (使用 existing async path, e.g. `fs/promises`).
- ❌ Don't add console output — keep helpers side-effect free.
