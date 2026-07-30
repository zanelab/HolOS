# @vben/locales Component Guidelines

> No Vue components. Source of truth = JSON locale files.

## Pattern

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

## Usage

```vue
<script setup>
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
<template>
  <h1>{{ t('page.home.title') }}</h1>
</template>
```

## Forbidden

- Don't put strings in Vue components
- Don't use Chinese / English strings directly
