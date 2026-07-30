# @vben/types Directory Structure

> 纯常量 / 类型 / preferences 工具包。

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
- **兼容 tree-shake** —— 每个导出单独命名

## 禁止

- 不要添加 Vue 代码
- 不要引入运行时依赖
- 不要打包到类 / 命名空间中
