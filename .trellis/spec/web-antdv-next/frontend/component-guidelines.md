# web-antdv-next Component Guidelines

> Vue 3 + vue + ant-design-vue conventions.

## Conventions

- **`<script setup lang="ts">`** only
- **`ant-design-vue v4`** components are imported **only** through `src/adapter/`
- **`<VbenForm>`** + **`<VbenVxeGrid>`** from @vben/common-ui + @vben/plugins/vxe-table
- **i18n** via `$t('namespace.key')` — never hard-code Chinese / English
- **Async route components**: `() => import('#/views/foo.vue')`

## Example: analytics view (paraphrase from real source)

```vue
<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { fetchAnalytics } from '#/api';
import { usePreferences } from '@vben/preferences';

const loading = ref(false);
const data = ref<AnalyticsData[]>([]);

onMounted(async () => {
  loading.value = true;
  data.value = await fetchAnalytics();
  loading.value = false;
});
</script>

<template>
  <Page>
    <Card :title="$t('page.dashboard.analytics')">
      <VChart :option="chartOption" />
    </Card>
  </Page>
</template>
```

## `ant-design-vue v4` Adapter Style

```ts
// src/adapter/component/index.ts (sample)
import { message, notification } from 'ant-design-vue v4';

export const tMessage = {
  loading: (opts) => message.loading(opts),
  success: (opts) => message.success(opts),
  error: (opts) => message.error(opts),
};

export const tNotification = {
  info: (opts) => notification.info(opts),
  success: (opts) => notification.success(opts),
  warning: (opts) => notification.warning(opts),
  error: (opts) => notification.error(opts),
};
```

Usage:

```ts
// in view
import { tMessage } from '#/adapter';

tMessage.success('保存成功');
```

## Naming Conventions

| Thing | Convention |
|---|---|
| Page file | `PascalCase.vue` |
| Component | `kebab-case.vue` |
| Composable | `useCamelCase` |
| Utility | `kebab-case.ts` |

## Forbidden

- ❌ Don't import `ant-design-vue v4` directly from views
- ❌ Don't mutate props in <script setup>
- ❌ Don't use v-html (XSS)
- ❌ Don't use defineComponent(Ellipsis)
- ❌ Don't inline i18n strings — always go through $t
- ❌ Don't ship features that depend on real backend unless backend-mock is running
