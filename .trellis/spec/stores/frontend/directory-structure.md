# @vben/stores Directory Structure

> Pinia stores shared across all web-* apps.

## 目录树 (verified from packages/stores/)

```
@vben/stores/
├── package.json                # name "@vben/stores" v5.7.0
├── tsconfig.json
├── setup.ts                    # createPinia + plugins
├── index.ts                    # re-exports stores
└── modules/
    ├── access.ts               # useAccessStore
    ├── auth.ts                 # useAuthStore
    └── user.ts                 # useUserStore
```

## 约定

- **One store per module file**
- **Setup-style stores** (defineStore("id", () => ...))
- **All stores registered in index.ts**

## 禁止

- Don't put business logic in setup()
- Don't put API calls inside setup()
- Don't create circular deps between stores
