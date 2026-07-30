# @vben/styles Directory Structure

> 针对每个框架 CSS bundle + global styles.

## 目录树 (verified from packages/styles/)

```
@vben/styles/
├── package.json                # name "@vben/styles" v5.7.0
├── index.ts                    # re-exports all flavors
├── style-exports.d.ts          # CSS module declarations
└── <flavor>/                   # per-UI-framework styles
    ├── antd/
    ├── ele/
    ├── naive/
    ├── antdv-next/
    └── global/
```

## 约定

- **Per-flavor subdirs** isolated by UI framework
- **global/** 用于跨父子集工具
- **style-exports.d.ts** - CSS module .d.ts

## 禁止

- 不要引入其他框架的组件
- 不要重新定义 Tailwind tokens
- Don't add JS to .css / .scss
