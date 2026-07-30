# @vben/stores Type Safety

> 严格模式 TS.

```ts
import { ref } from 'vue';
import { defineStore } from 'pinia';
export const useAccessStore = defineStore('access', () => {
  const x = ref(null);
  return { x };
});
```
