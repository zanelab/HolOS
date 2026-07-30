# shared Quality Guidelines

> **PLACEHOLDER DOCS** - 本包 does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. 替换这些文件 real content when package 添加后.

## 预期代码风格

- 4 spaces TS / Vue indent
- Single quotes TS; double quotes HTML
- No semicolons (OxFmt auto-format)
- Max line length 120
- Trailing newline required

## 预期命名

| Thing | Convention |
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
- Commitlint (feat(): / fix(): / chore():)

## 禁止

- 不要 use any
- 不要 add @ts-ignore without comment
- 不要 commit .env or secrets
- 不要 implement against this phantom package
