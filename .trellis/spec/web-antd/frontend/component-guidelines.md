# @vben/web-antd Component Guidelines

> Vue 3 +  Ant Design Vue (vben flavor) — see also `web-tdesign/component-guidelines.md` for shared conventions.

## 约定

- **`<script setup lang="ts">`** only
- **Ant Design Vue** imported through `src/adapter/antdv.ts`:
  ```ts
  import { message } from 'ant-design-vue';
  // wrapped via adapter
  export const tMessage = {
    loading: (opts) => message.loading(opts),
    success: (opts) => message.success(opts),
    error: (opts) => message.error(opts),
  };
  ```
- **i18n** via `$t('namespace.key')`
- **`<VbenForm>`** / **`<VbenVxeGrid>`** from `@vben/common-ui` + `@vben/plugins/vxe-table`
- **Async route components**: `() => import('#/views/foo.vue')`

## Preferences Extension Pattern

```ts
import { definePreferencesExtension } from '@vben/preferences';

interface WebAntdPreferencesExtension {
  defaultTableSize: number;
  enableFormFullscreen: boolean;
}

export const preferencesExtension = definePreferencesExtension<WebAntdPreferencesExtension>({
  tabLabel: 'preferences.antd.tabLabel',
  title: 'preferences.antd.title',
  fields: [
    {
      component: 'switch',
      defaultValue: true,
      key: 'enableFormFullscreen',
      label: 'preferences.antd.fields.enableFormFullscreen.label',
      tip: 'preferences.antd.fields.enableFormFullscreen.tip',
    },
  ],
});
```

## 禁止

- Don't import `ant-design-vue` directly from views
- Don't bypass `<VbenForm>` with raw `<a-form>`
- Don't add inline CSS — use Tailwind classes

## See Also

- `web-tdesign/component-guidelines.md` for shared patterns
- `web-holos/component-guidelines.md` (canonical example, first to be written)
