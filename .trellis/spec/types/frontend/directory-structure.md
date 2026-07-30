# @vben/types Directory Structure

> Pure constants/types/preferences utilities package.

## 目录树 (verified)

```
@vben/types/
├── package.json                # workspace name "@vben/types"
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
