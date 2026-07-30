# shadcn-ui 状态管理

> **PLACEHOLDER DOCS** - 本包 does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. 替换这些文件 real content when package 添加后.

## 预期决策树

| Where state lives | Use |
|---|---|
| One component | ref() / reactive() |
| Cross-page, persisted | preferences store (@vben/preferences) |
| Cross-page, transient | Pinia store (@vben/stores) |
| Server cache | API + useXResource pattern |

## 示例 (synthetic)

```ts
// Apps: use Pinia store
import { defineStore } from "pinia";
export const useXStore = defineStore("x", () => {
  const xList = ref<XItem[]>([]);
  return { xList };
});

// Libs: stateless, callers handle state
export function transformX(input: XInput): XOutput { /* pure */ }
```

## 禁止

- 不要 persist auth tokens in localStorage (XSS risk)
- 不要 use Vuex (this monorepo uses Pinia)
- 不要 mutate preferences outside the store API
