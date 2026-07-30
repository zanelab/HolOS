# @vben/stores "Component" Style - Pinia 状态

> 无 Vue 组件。 Stores = Pinia state + actions.

## 模式: setup-style store

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

## 用法

```vue
<script setup>
import { useAccessStore } from "@vben/stores";
const accessStore = useAccessStore();
accessStore.setAccessMenus(menus);
</script>
```

## 禁止

- Don't use Options API for stores
- Don't define globals outside defineStore
