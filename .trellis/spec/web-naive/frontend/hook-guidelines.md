# @vben/web-naive Custom Hooks

> 除非绝对必要，否则不要写新 hooks.

## 内置函数（始终优先检查）

| Concern | Hook | Source |
|---|---|---|
| App config | usePreferences() | @vben/preferences |
| Pinia stores | useAccessStore, useUserStore, useAuthStore | @vben/stores |
| i18n | useI18n() | vue-i18n |
| Router | useRouter(), useRoute() | vue-router |
| Form | useVbenForm() | @vben/common-ui |
| Table | useVbenVxeGrid() | @vben/plugins/vxe-table |

## 何时 Write a New Hook

- Used by >= 3 views / components
- Returns reactive state OR stable async function
- Non-trivial logic (> 10 lines)

## Convention

- use-<name>.ts (kebab-case, `use` prefix)
- Co-located for one-feature hooks; shared under src/hooks/

## 禁止

- Don't wrap usePreferences() in another useFoo()
- Don't put pure business logic in a hook
- Don't use hooks outside <script setup>
