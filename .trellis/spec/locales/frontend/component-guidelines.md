# @vben/locales Component Guidelines

> 无 Vue 组件。 Source of truth = JSON locale files.

## 模式

```json
{
  "auth": {
    "login": "Login"
  },
  "page": {
    "home": {
      "title": "Home"
    }
  }
}
```

## 用法

```vue
<script setup>
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
<template>
  <h1>{{ t('page.home.title') }}</h1>
</template>
```

## 禁止

- Don't put strings in Vue components
- Don't use Chinese / English strings directly
