# @vben/web-antdv-next Custom Hooks

> 除非绝对必要，否则不要编写新的 hooks。

## 内置函数（始终优先检查）

| Concern | Hook | Source |
|---|---|---|
| App config | usePreferences() | @vben/preferences |
| Pinia stores | useAccessStore, useUserStore, useAuthStore | @vben/stores |
| i18n | useI18n() | vue-i18n |
| Router | useRouter(), useRoute() | vue-router |
| Form | useVbenForm() | @vben/common-ui |
| Table | useVbenVxeGrid() | @vben/plugins/vxe-table |

## 何时编写新 Hook

- 被 ≥ 3 个 views / components 使用
- Returns reactive state OR stable async function
- 非平凡逻辑（> 10 行）

## 约定

- use-<name>.ts (kebab-case, `use` prefix)
- Co-located for one-feature hooks; shared under src/hooks/

## 禁止

- Don't wrap usePreferences() in another useFoo()
- 不要将纯业务逻辑写在 hook 中
- 不要在 <script setup> 之外使用 hooks
