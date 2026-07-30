# @vben/utils Directory Structure

> Pure utility package - no UI, no Vue, no runtime.

## 目录树 (verified from packages/utils/)

```
@vben/utils/
├── package.json                # workspace name "@vben/utils"
├── tsconfig.json
├── index.ts                    # public barrel
└── helpers/                    # various helper modules
```

## 约定

- **Single barrel** at index.ts
- **Pure functions** only - no IO
- **测试放在 __tests__/与源码同位**

## 禁止

- Don't add Vue code
- 不要添加副作用
