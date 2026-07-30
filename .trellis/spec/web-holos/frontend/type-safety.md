# Web-Holos Type Safety

## 约定

- `tsconfig.json` extends `@vben/tsconfig/web-app.json`
- 严格模式 **ON** by default
- All entry points (`main.ts`, `bootstrap.ts`, `App.tsx`, route components, store factories) **must** be strongly typed
- `vue-tsc --noEmit --skipLibCheck` is the typecheck command

## Type imports

```ts
import type { RouteRecordRaw } from 'vue-router';
import type { ComponentRecordType, GenerateMenuAndRoutesOptions } from '@vben/types';
```

## Type safety rules

- Use `unknown` for genuinely unknown values (then narrow with `instanceof` / type guards)
- Use `as const` for literal objects
- Avoid `as` cast; prefer refactor

## 禁止

- ❌ Don't use `any`. If framework types force a cast, use `Recordable<unknown>` and cast in one place
- ❌ Don't disable strict mode per-file with `// @ts-nocheck`
- ❌ Don't add `@ts-ignore` or `@ts-expect-error` without a justified comment
