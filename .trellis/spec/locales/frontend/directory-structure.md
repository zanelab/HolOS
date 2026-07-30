# @vben/locales Directory Structure

> i18n locales package - vue-i18n source of truth.

## 目录树 (verified)

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

## 约定

- **Top-level keys**: auth, common, demos, page - each maps to its own JSON
- **Nested keys** allowed: page.home.title, demos.vben.title
- **两种语言在同一次提交中同时更新**
- **fallbackLocale** is en-US

## 禁止

- 不要在 Vue 组件中写硬编码的 i18n 字符串
- 不要在此处放翻译逻辑
