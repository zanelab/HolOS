# Web-Holos Quality Guidelines

> Adopted from the team's `commitlint-config` + `eslint-config` + TDesign Vue best practices.

## 代码风格

- **4 spaces indent**, 2-space JSX
- **Single quotes** for strings, **double quotes** for JSX/HTML attributes
- **No semicolons in JS** if using Vben default (`@vben/eslint-config`) — keep that consistent
- **Trailing newline** required at end of every file
- **Max line length** 120 (ESLint default)

## 命名约定

- Components / Vue files: `PascalCase.vue` for pages, `kebab-case.vue` for parts
- Composables: `useCamelCase`
- Utility: `kebab-case.ts`
- Constants: `UPPER_SNAKE_CASE`

## 禁止

- ❌ Don't use `any` — use `unknown` + narrowing or define a typed interface
- ❌ Don't use `@ts-ignore` — fix the type, or refactor to a `// @ts-expect-error` with a comment
- ❌ Don't commit `.env`, tokens, or API keys
- ❌ Don't use `console.log` for production diagnostics — use `logger` package
- ❌ Don't bypass committed hooks (pre-commit / pre-push)

## Commit Messages (commitlint)

`feat(web-holos): ...` / `fix(web-holos): ...` / `chore: ...`

Scopes accepted: `web-holos`, `web-tdesign`, `web-antd`, etc.
