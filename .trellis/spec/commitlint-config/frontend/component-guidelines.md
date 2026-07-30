# @vben/commitlint-config Component Guidelines

> Conventional Commits config — typed config object.

## Pattern: UserConfig with strict rules

```ts
import type { UserConfig } from '@commitlint/types';

export default {
  extends: ['@commitlint/config-conventional'],
  parserPreset: {
    parserOpts: {
      headerPattern: /^(\w*)(?:\((.*)\))?!?: (.*)$/,
      headerCorrespondence: ['type', 'scope', 'subject'],
    },
  },
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', /* ... */]],
    'subject-empty': [2, 'never'],
    'type-max-length': [2, 'always', 72],
  },
} satisfies UserConfig;
```

## Usage in apps

```ts
// apps/web-holos/commitlint.config.ts
import config from '@vben/commitlint-config';
export default config;
```

Or in `package.json`:
```json
{
  "commitlint": {
    "extends": ["@vben/commitlint-config"]
  }
}
```

## Naming

| Element | Convention | Example |
|---|---|---|
| Type | lowercase noun | feat, fix, docs, refactor |
| Scope | lowercase path-ish | web-holos, router, locales |
| Subject | imperative present | add dashboard route |

## Tree-shake

```ts
// ✅ Re-export from index only
import config from '@vben/commitlint-config';

// ❌ Don't deep-import
import rules from '@vben/commitlint-config/rules';
```

## Forbidden

- ❌ 不要 modify accepted `type-enum` — 11 个 types 固定
- ❌ 不要 bypass `extends: ['@commitlint/config-conventional']`
- ❌ 不要修改 header max length — 72 by Debian + GitHub convention
- ❌ 不要 commit `WIP` title — use `chore(wip):` instead
- ❌ 不要 use `init` type (doesn't exist in conventional commits)
- ❌ 不要在 scope 里用 Capital Letters
