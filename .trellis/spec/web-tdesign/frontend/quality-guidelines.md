# @vben/web-tdesign Quality Guidelines

> Adopted from the team's `commitlint-config` + `eslint-config` + `oxlint-config` + `stylelint-config` chain.

## 代码风格

- **4 spaces** indent (TS / Vue template). HTML attributes: 2 spaces.
- **Single quotes** for TS strings; **double quotes** for HTML attributes
- **No semicolons in TS** — leverage the auto-formatter on commit (OxFmt)
- **Trailing newline** at end of every file (`*.editorconfig` enforces)
- **Max line length**: 120 chars (`@vben/eslint-config` default)

## 命名约定

| Thing | Convention | Example |
|---|---|---|
| Vue page file | `PascalCase.vue` | `Analytics.vue` |
| Vue part/component | `kebab-case.vue` | `menu-item.vue` |
| Composable / hook | `useCamelCase` | `useAsyncResource` |
| Pure utility | `kebab-case.ts` | `merge-route-modules.ts` |
| Pinia store | `useXxxStore` | `useAccessStore` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| File tree | `<package>/<role>` | `core.ts`, `modules/dashboard.ts` |

## 提交前钩子 (auto-fired)

- **OxLint** — fast lint, replaces ESLint for most rules
- **OxFmt** — auto-formatter (runs on staged files)
- **ESLint** — for rules OxLint doesn't cover
- **Stylelint** — CSS / SCSS / Vue `<style>` lint
- **Commitlint** — `feat():` / `fix():` / `chore():` prefix enforced

## 禁止

- ❌ Don't use `any` — use `unknown` + narrow, or define a typed interface.
- ❌ Don't add `@ts-ignore` without a justified `// why: ...` comment.
- ❌ Don't bypass any pre-commit hook with `--no-verify` (off by default — manual override only).
- ❌ Don't commit `.env`, `*.local`, secret files.
- ❌ Don't use `console.log` for production diagnostics — use the `logger` package or structured logging.
- ❌ Don't commit `node_modules`, `dist`, `.vite` — already in `.gitignore` but worth noting.

## Lint / 类型检查 Commands

```bash
pnpm typecheck                       # vue-tsc --noEmit --skipLibCheck
pnpm lint                            # runs OxLint + ESLint via turbo
pnpm lint:fix                        # auto-fix what OxLint can
```
