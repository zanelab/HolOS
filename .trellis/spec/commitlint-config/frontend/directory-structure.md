# @vben/commitlint-config Directory Structure

> Real config for Conventional Commits. Source verified 2026-07-30.

## 目录树

```
@vben/commitlint-config/             # workspace: internal/lint-configs/commitlint-config/
├── package.json                     # name "@vben/commitlint-config" v5.7.0
├── tsconfig.json
└── src/
    ├── index.ts                     # re-exports rules + parserOptions
    └── rules/                        # (optionally split by scope)
```

## 实际源码参考

`internal/lint-configs/commitlint-config/index.ts` (verified):

```ts
import type { UserConfig } from '@commitlint/types';

/**
 * HolOS monorepo commit conventions:
 * - type(scope): subject
 * - body optional
 * - footer optional (e.g., BREAKING CHANGE: ...)
 */
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2, 'always', [
        'feat',     // 新功能
        'fix',      // bug 修复
        'docs',     // 文档
        'style',    // 格式
        'refactor', // 重构
        'perf',     // 性能
        'test',     // 测试
        'build',    // 构建
        'ci',       // CI 配置
        'chore',    // 杂项
        'revert',   // 回滚
      ],
    ],
    'type-min-length': [2, 'always', 10],
    'type-max-length': [2, 'always', 72],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 72],
    'body-leading-blank': [2, 'always'],
    'footer-leading-blank': [2, 'always'],
  },
} satisfies UserConfig;
```

## Conventions

- **Conventional Commits** 严格遵循
- **Type enum** 限定 11 个 accepted types
- **Subject length** 限制 10-72 chars
- **No period at subject end**
- **Body line** 必须 blank line 后开始

## Commit Examples

```bash
# ✅ Good
git commit -m "feat(web-holos): add dashboard route"
git commit -m "fix(router): handle null user info"
git commit -m "docs: update README"

# ❌ Bad
git commit -m "Added stuff"           # no type: scope:
git commit -m "feat(web-holos). Add dashboard route."  # period + 72+ chars
git commit -m "FEAT: stuff"           # type uppercase
```

## Forbidden

- ❌ 不要用 `feat` / `fix` 之外 types(除非已在 enum)
- ❌ 不要在 type 后不加 scope(`feat: x` — 只要单 module changes)
- ❌ 不要 commit title > 72 chars
- ❌ 不要结尾加 `.` 在 subject
- ❌ 不要 skip commitlint hook via --no-verify(只重要 commits override)

## Integration

`apps/web-holos/.lefthook.yml`:
```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm exec commitlint --edit
```
