# @vben/web-naive Component Guidelines

> Vue 3 +  UI-framework conventions.

## 约定

- **<script setup lang="ts">** only
- **UI-framework** imported through adapters
- **i18n** via $t("namespace.key")
- **<VbenForm>** + **<VbenVxeGrid>** from @vben/common-ui + @vben/plugins/vxe-table

## 示例: analytics view

```vue
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchAnalytics } from "#/api";
const data = ref<AnalyticsData[]>([]);
onMounted(async () => { data.value = await fetchAnalytics(); });
</script>
<template>
  <Page>
    <Card :title="$t('page.dashboard.analytics')">
      <VChart :option="chartOption" />
    </Card>
  </Page>
</template>
```

## 禁止

- Don't import UI lib directly from views
- Don't mutate props in <script setup>
- Don't use v-html (XSS)
- Don't use defineComponent({...})
