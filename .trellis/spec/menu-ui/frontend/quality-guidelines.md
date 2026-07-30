# menu-ui Quality Guidelines

> **PLACEHOLDER DOCS** - This package does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. Replace these files with real content when the package is added.

## Expected Style

- 4 spaces TS / Vue indent
- Single quotes TS; double quotes HTML
- No semicolons (OxFmt auto-format)
- Max line length 120
- Trailing newline required

## Expected Naming

| Thing | Convention |
|---|---|
| Vue page file | PascalCase.vue |
| Component | kebab-case.vue |
| Composable | useCamelCase |
| Pinia store | useXxxStore |
| Constant | UPPER_SNAKE_CASE |

## Pre-commit Hooks

- OxLint (fast)
- OxFmt (formatter)
- ESLint (rules OxLint misses)
- Stylelint (CSS / Vue style)
- Commitlint (feat(): / fix(): / chore():)

## Forbidden

- Do not use any
- Do not add @ts-ignore without comment
- Do not commit .env or secrets
- Do not implement against this phantom package
