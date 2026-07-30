# @vben/constants Directory Structure

> Pure constants/types/preferences utilities package.

## 目录树（已核对）

```
@vben/constants/
├── package.json                # workspace name "@vben/constants"
├── tsconfig.json
└── src/
    ├── index.ts                # public barrel
    └── (constants.ts | types.ts | config.ts)
```

## 约定

- **Single barrel** at index.ts
- **Pure values/types only** - no IO
- **Tree-shake friendly** - each export individually named

## 禁止

- Don't add Vue code
- Don't import runtime dependencies
- Don't bundle into classes / namespaces
