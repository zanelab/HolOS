# layout-ui State Management

> **PLACEHOLDER DOCS** - This package does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. Replace these files with real content when the package is added.

## Expected Decision Tree

| Where state lives | Use |
|---|---|
| One component | ref() / reactive() |
| Cross-page, persisted | preferences store (@vben/preferences) |
| Cross-page, transient | Pinia store (@vben/stores) |
| Server cache | API + useXResource pattern |

## Example (synthetic)

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

## Forbidden

- Do not persist auth tokens in localStorage (XSS risk)
- Do not use Vuex (this monorepo uses Pinia)
- Do not mutate preferences outside the store API
