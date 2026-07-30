# @vben/locales Component Guidelines

> No Vue components in this package. All Vue integration happens via `vue-i18n`.

## Purpose

`@vben/locales` does not ship Vue SFCs. It only owns the i18n instance and
message dictionaries. Components in `apps/web-*/src/views/**` use `useI18n()`
or the `$t` global to render translated strings.

## Translation Component Pattern

Most apps use the `I18nT` composable or `<i18n-t>` for inline interpolation:

```vue
<!-- apps/web-antdv-next/src/views/authentication/login.vue (real) -->
<script setup lang="ts">
import { $t } from '#/locales';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const formRules = {
  username: [
    {
      message: t('authentication.usernameRequired'),
      required: true,
      trigger: ['blur', 'input'],
    },
  ],
};

const handleSubmit = async () => {
  // ...
  notification.success({
    title: $t('authentication.loginSuccess'),
    description: `${$t('authentication.loginSuccessDesc')}: ${userInfo.realName}`,
  });
};
</script>
```

## Templates that need pluralisation

```vue
<i18n-t keypath="authentication.welcomeBack" scope="global">
  <template #userName>
    <span class="text-primary">{{ userInfo.realName }}</span>
  </template>
</i18n-t>
```

## Real `langs/en-US/authentication.json` excerpt

```json
{
  "loginSuccess": "Login successful",
  "loginSuccessDesc": "Welcome back",
  "usernameRequired": "Please enter username",
  "passwordRequired": "Please enter password",
  "welcomeBack": "Welcome back, {userName}"
}
```

## Conventions

- **One namespace per JSON file** — never inline strings into a "misc.json".
- **Translation keys** use `camelCase` segments; nested allowed
  (`page.home.title`).
- **Plural / interpolation** uses named placeholders (`{userName}`), not
  positional `%s`.
- **Component-side fallback** when key missing: `i18n.global.setMissingHandler`
  logs a `[intlify] Not found` warning.
- **Apps** must import `$t` from `#/locales` (the local re-export), not
  directly from `@vben/locales`.
- **No `<i18n>` block** in SFCs — defer to JSON files for translation.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Translation key | `camelCase` | `loginSuccess` |
| Namespace file | `kebab-case.json` | `authentication.json` |
| Interpolation | `{namedPlaceholder}` | `{userName}` |
| Missing handler flag | `missingWarn: true` | — |

## Forbidden

- ❌ 不要 inline HTML strings with `v-html` for translations — XSS
- ❌ 不要 `t('literal English string')` — every key needs an entry in JSON
- ❌ 不要 couple component code with `langs/**/*.json` — pure data layer
- ❌ 不要 put colour / layout strings in locales — that's UI config
- ❌ 不要 use `tc()` (legacy mode) — `legacy: false` is set in `createI18n`
- ❌ 不要 import i18n chains via `vue-i18n` raw — use this package's barrel
