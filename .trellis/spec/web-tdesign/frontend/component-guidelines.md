# @vben/web-tdesign Component Guidelines

> Conventions for Vue components in TDesign-Vue flavor apps (real layout verified from `apps/web-tdesign/src/`).

## Conventions

- **`<script setup lang="ts">` only**. No Options API.
- **TDesign components** are imported through adapters under `src/adapter/component/`. Example (from `src/adapter/tdesign.ts`):
  ```ts
  import { MessagePlugin } from 'tdesign-vue-next';
  // ... adapter wraps MessagePlugin.loading / success / error
  export const message = {
    loading: (opts) => MessagePlugin.loading(opts),
    success: (opts) => MessagePlugin.success(opts),
    error: (opts) => MessagePlugin.error(opts),
  };
  ```
- **`<t-table>` / `<t-form>`** integration goes through `<VbenForm>` / `<VbenVxeGrid>` from `@vben/common-ui` + the `@vben/plugins/vxe-table` adapter (see `src/adapter/vxe-table.ts`).
- **i18n keys** go through `$t('namespace.key')`. Never hard-code Chinese / English strings.
- **Async components**: `<script setup>` + `defineAsyncComponent(() => import('./foo.vue'))` when needed; route-level async via `() => import('#/views/foo.vue')`.

## Example: a real page from this app (`src/views/dashboard/analytics/index.vue`)

Real code (paraphrased — full file is ~80 lines):

```vue
<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { fetchAnalytics } from '#/api';
import { usePreferences } from '@vben/preferences';

const loading = ref(false);
const data = ref<AnalyticsData[]>([]);
const preferences = usePreferences();

const chartOptions = computed(() => ({
  xAxis: { type: 'category', data: data.value.map(d => d.label) },
  yAxis: { type: 'value' },
  series: [{ type: 'line', data: data.value.map(d => d.value) }],
}));

onMounted(async () => {
  loading.value = true;
  data.value = await fetchAnalytics();
  loading.value = false;
});
</script>

<template>
  <Page>
    <Card :title="$t('page.dashboard.analytics')">
      <VChart :option="chartOptions" />
    </Card>
  </Page>
</template>
```

## Forbidden

- ❌ Don't import TDesign directly in views — go through the adapter.
- ❌ Don't mutate props inside `<script setup>` (Vue 3 reactivity is one-way).
- ❌ Don't use v-html in templates unless content is fully sanitized (XSS vector).
- ❌ Don't `defineComponent({ ... })` — use `<script setup>` syntax sugar.
- ❌ Don't add new `<style scoped>` global resets — use `@vben/styles` for design tokens.
