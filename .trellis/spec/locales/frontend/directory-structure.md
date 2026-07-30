# @vben/locales Directory Structure

> i18n locales package - vue-i18n source of truth.

## Tree (verified)

```
@vben/locales/
├── package.json                # name "@vben/locales" v5.7.0
├── tsconfig.json
├── i18n.ts                     # $t wrapper
├── typing.ts                   # locale types
├── index.ts                    # setupI18n + loadMessages
└── langs/
    ├── zh-CN/
    │   ├── auth.json
    │   ├── common.json
    │   ├── demos.json
    │   └── page.json
    └── en-US/...
```

## Conventions

- **Top-level keys**: auth, common, demos, page - each maps to its own JSON
- **Nested keys** allowed: page.home.title, demos.vben.title
- **Both languages land in same commit**
- **fallbackLocale** is en-US

## Forbidden

- Don't put i18n strings in Vue components
- Don't put translation logic here
