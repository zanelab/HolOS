# @vben/web-naive Quality Guidelines

> Strict-mode TS + 4-space + OxLint + ESLint + Stylelint + Commitlint.

## Style

- 4 spaces indent
- Single quotes TS; double quotes HTML
- No semicolons
- Max line 120
- Trailing newline

## Naming

| Thing | Convention |
|---|---|
| Page file | PascalCase.vue |
| Component | kebab-case.vue |
| Composable | useCamelCase |
| Utility | kebab-case.ts |
| Pinia store | useXxxStore |
| Constant | UPPER_SNAKE_CASE |

## Forbidden

- Don't use any
- Don't add @ts-ignore without comment
- Don't bypass hooks with --no-verify
- Don't commit .env or secrets
