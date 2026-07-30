# web-ele Quality Guidelines

> Strict-mode TS + 4-space + OxLint + ESLint + Stylelint + Commitlint.

## Coding Style

- **4 spaces** TS / Vue indent
- **Single quotes** TS; **double quotes** HTML
- **No semicolons** in TS
- **Max line length** 120
- **Trailing newline** required

## Naming

| Thing | Convention |
|---|---|
| Vue page file | `PascalCase.vue` |
| Component | `kebab-case.vue` |
| Composable | `useCamelCase` |
| Utility | `kebab-case.ts` |
| Pinia store | `useXxxStore` |
| Constant | `UPPER_SNAKE_CASE` |

## Pre-commit Hooks (auto-fired)

- **OxLint** — fast lint
- **OxFmt** — auto-formatter (staged files)
- **ESLint** — for rules OxLint misses
- **Stylelint** — CSS / Vue `<style>` lint
- **Commitlint** — `feat():` / `fix():` / `chore():` enforced

## element-plus 风格 Notes

- Use element-plus 符合 framework idiomatic patterns
- Don't mix Reactive frameworks(Vue 3 only here)
- Theme 切换: prefer `<element-plusConfigProvider>` over manual CSS

## Forbidden

- ❌ Don't use `any` (use `unknown` + narrow)
- ❌ Don't add `@ts-ignore` without `// why:` comment
- ❌ Don't bypass pre-commit hooks with `--no-verify`
- ❌ Don't commit `.env`, `*.local`, secrets
- ❌ Don't use `console.log` for production diagnostics
- ❌ Don't mix `web-tdesign` package imports in this app's source
- ❌ Don't write app-specific CSS that should go to `src/index.css`
