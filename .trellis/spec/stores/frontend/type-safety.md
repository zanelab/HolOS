# @vben/stores Type Safety

> Strict-mode TS.

```ts
import { ref } from 'vue';
import { defineStore } from 'pinia';
export const useAccessStore = defineStore('access', () => {
  const x = ref(null);
  return { x };
});
```
