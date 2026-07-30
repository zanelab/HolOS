# @vben/oxfmt-config Directory Structure

> 仅含配置的包，通过工作区别名引用。

## 目录树 (verified)

```
@vben/oxfmt-config/
├── package.json                # workspace name "@vben/oxfmt-config"
├── tsconfig.json
└── src/
    ├── index.ts                # re-exports everything
    └── (one or more config files)
```

## 约定

- **配置对象** 以命名 const 导出
- **Single barrel** at src/index.ts
- **无真实构建步骤** —— 通过 tsx 直接消费
- **scripts/stub.mjs** provides fake dist/index.mjs

## 禁止

- Don't add runtime code (HTTP, file IO, async)
- Don't add CLI
- Don't add tests
