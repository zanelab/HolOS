# @vben/web-ele Quality Guidelines

> 严格模式 TS + 4-space + OxLint + ESLint + Stylelint + Commitlint.

## 代码风格

- 使用 4 空格缩进
- Single quotes TS; double quotes HTML
- 不使用分号
- 单行最大长度 120
- Trailing newline

## 命名约定

| Thing | Convention |
|---|---|
| Page file | PascalCase.vue |
| Component | kebab-case.vue |
| Composable | useCamelCase |
| Utility | kebab-case.ts |
| Pinia store | useXxxStore |
| Constant | UPPER_SNAKE_CASE |

## 禁止

- Don't use any
- Don't add @ts-ignore without comment
- Don't bypass hooks with --no-verify
- 不要提交 .env 或密钥
