# @vben/node-utils "Component" Style — Function Helpers

> 本包 doesn't ship Vue components. Its "components" are **pure functions**.

## 模式：单导出函数辅助器

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

## 在下游应用中的用法

```ts
import { formatBytes, formatDuration } from '@vben/node-utils';

console.log(formatBytes(1024 * 1024));       // "1 MB"
console.log(formatDuration(123456));        // "2m 3s"
```

## 禁止

- ❌ 不要将函数打包到类或命名空间对象中（会丧失 tree-shaking）。
- ❌ 除非必要不要在顶层 import Node 内置模块 — 保持 import 粗尝。
- ❌ Don't add async variants of pure sync helpers (使用 existing async path, e.g. `fs/promises`).
- ❌ 不要输出控制台内容 — 保持辅助函数无副作用。
