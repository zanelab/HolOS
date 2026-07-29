# @vben/web-antdv-next Custom Hooks

> Don't write new hooks unless absolutely necessary.

## Built-ins (always check first)

| Concern | Hook | Source |
|---|---|---|
| App config | usePreferences() | @vben/preferences |
| Pinia stores | useAccessStore, useUserStore, useAuthStore | @vben/stores |
| i18n | useI18n() | vue-i18n |
| Router | useRouter(), useRoute() | vue-router |
| Form | useVbenForm() | @vben/common-ui |
| Table | useVbenVxeGrid() | @vben/plugins/vxe-table |

## When to Write a New Hook

- Used by >= 3 views / components
- Returns reactive state OR stable async function
- Non-trivial logic (> 10 lines)

## Convention

- use-<name>.ts (kebab-case, `use` prefix)
- Co-located for one-feature hooks; shared under src/hooks/

## Forbidden

- Don't wrap usePreferences() in another useFoo()
- Don't put pure business logic in a hook
- Don't use hooks outside <script setup>
