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

- **一个模块文件一个 store**
- **Setup-style stores** (defineStore("id", () => ...))
- **All stores registered in index.ts**

## 禁止

- 不要在 setup() 中放业务逻辑
- Don't put API calls inside setup()
- store 与 store 之间不要产生环状依赖
