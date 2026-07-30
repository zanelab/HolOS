# @vben/styles Directory Structure

> Per-framework CSS bundle + global styles.

## Tree (verified from packages/styles/)

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

## Conventions

- **Per-flavor subdirs** isolated by UI framework
- **global/** for cross-flavor utilities
- **style-exports.d.ts** - CSS module .d.ts

## Forbidden

- Don't import other framework's components
- Don't redefine Tailwind tokens
- Don't add JS to .css / .scss
