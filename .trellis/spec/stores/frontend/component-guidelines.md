# @vben/stores "Component" Style - Pinia Stores

> No Vue components. Stores = Pinia state + actions.

## Pattern: setup-style store

```ts
import { defineStore } from "pinia";
export const useAccessStore = defineStore("access", () => {
  const accessToken = ref<AccessToken>(null);
  function setAccessMenus(menus: RouteRecordStringComponent[]) {
    accessMenus.value = menus;
  }
  return { accessToken, setAccessMenus };
});
```

## Usage

```vue
<script setup>
import { useAccessStore } from "@vben/stores";
const accessStore = useAccessStore();
accessStore.setAccessMenus(menus);
</script>
```

## Forbidden

- Don't use Options API for stores
- Don't define globals outside defineStore
