# @core Quality Guidelines

> **PLACEHOLDER DOCS** - 本包 does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. 替换这些文件 real content when package 添加后.

## 预期代码风格

- 4 spaces TS / Vue indent
- Single quotes TS; double quotes HTML
- No semicolons (OxFmt auto-format)
- 单行最大长度 120
- 文件末尾必须有换行符

## 预期命名

| 事项 | 约定 |
|---|---|
| Vue page file | PascalCase.vue |
| Component | kebab-case.vue |
| Composable | useCamelCase |
| Pinia store | useXxxStore |
| Constant | UPPER_SNAKE_CASE |

## 提交前钩子

- OxLint (fast)
- OxFmt (formatter)
- ESLint (rules OxLint misses)
- Stylelint (CSS / Vue style)
- Commitlint（feat(): / fix(): / chore():）

## 禁止

- 不要使用 any
- 不要 add @ts-ignore without comment
- 不要提交 .env 或密钥
- 不要针对这个幻影包进行实现
