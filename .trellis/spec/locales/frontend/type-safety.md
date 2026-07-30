# @vben/locales Type Safety

> Locales typed via vue-i18n.

```ts
declare module 'vue-i18n' {
  interface DefineLocaleMessage { auth: typeof enUS.auth; page: typeof enUS.page; }
}
```

## 禁止

- Don't use any
- Don't import raw JSON in app code
