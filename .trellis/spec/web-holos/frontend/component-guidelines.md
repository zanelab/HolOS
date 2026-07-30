# Web-Holos 组件规范

> Vue 3 +  TDesign Vue Next conventions for `apps/web-holos/` components

## 约定

- **Functional `.vue` files** default. Use `<script setup lang="ts">`
- **Composition API**: `ref` / `reactive` / `computed` / `watchEffect`
- **TDesign**: import components from `tdesign-vue-next`
- **i18n**: import from `#/locales`, use `t('namespace.key')`
- **Async imports**: router-level code uses dynamic `() => import('./views/foo.vue')`
- **插槽**：优先使用命名插槽，而非模糊的默认插槽

## 示例 home component (`src/views/home/index.vue`)

```vue
<script lang="ts" setup>
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>

<template>
  <div class="holos-home">
    <header class="holos-home__header">
      <h1 class="holos-home__title">HolOS</h1>
      <p class="holos-home__subtitle">{{ t('page.home.tagline') }}</p>
    </header>
    <section class="holos-home__content">
      <p class="holos-home__hint">{{ t('page.home.ready') }}</p>
    </section>
  </div>
</template>

<style scoped>
.holos-home { display: flex; flex-direction: column; ... }
</style>
```

## 禁止

- ❌ Don't use Vue 2 options API
- ❌ 不要全局 import tdesign — 按组件单独 import
- ❌ Don't use absolute paths in `router/routes/` modules — use `#/*` alias
- ❌ Don't inline i18n strings — always go through `t(...)`
- ❌ 不要 ship 依赖真实 backend 的功能，除非 backend-mock 正在运行
