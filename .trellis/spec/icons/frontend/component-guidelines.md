# @vben/icons Component Guidelines

## Pattern: IconifyIcon wrapper

```vue
<script setup lang="ts">
import { Icon } from '@iconify/vue';
defineProps<{ icon: string; size?: number }>();
</script>
<template>
  <Icon :icon="icon" :width="size ?? 16" :height="size ?? 16" />
</template>
```

Usage:

```vue
<IconifyIcon icon="lucide:home" :size="20" />
```

## Forbidden

- Don't import raw icons from Iconify / @iconify/vue directly
- Don't add <svg> inline to views
