# @vben/preferences Directory Structure

> Pure constants/types/preferences utilities package.

## Tree (verified)

```
@vben/preferences/
├── package.json                # workspace name "@vben/preferences"
├── tsconfig.json
└── src/
    ├── index.ts                # public barrel
    └── (constants.ts | types.ts | config.ts)
```

## Conventions

- **Single barrel** at index.ts
- **Pure values/types only** - no IO
- **Tree-shake friendly** - each export individually named

## Forbidden

- Don't add Vue code
- Don't import runtime dependencies
- Don't bundle into classes / namespaces
