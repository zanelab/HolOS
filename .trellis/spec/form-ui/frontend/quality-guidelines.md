# form-ui — PLACEHOLDER SPEC

**Expected package:** `@vben-core/form-ui` — VbenForm wrappers around naive-ui / shadcn-vue form primitives — `Form`, `FormItem`, `FormApi`, validation adapters, schema-driven forms.

> ⚠️ **PLACEHOLDER DOCS** — This package does **not** exist in the current
> workspace. The structure, conventions, and code examples below are
> best-guess projections based on the upstream `vben v5.7.0` monorepo
> (`vbenjs/vben-admin-monorepo`) and the role this package plays
> in a real vben app. **Replace this file with real content when (and
> only when) the corresponding `packages/form-ui/`
> directory lands upstream.**

Do **not** implement against this placeholder — code that imports from
`@vben-core/form-ui` will fail to typecheck.
## Code style

- **4-space** TS / Vue indent (2-space for SVG / CSS).
- **Single quotes** for TS strings, **double quotes** for HTML.
- **No semicolons** (OxFmt auto-inserts them on commit).
- **120-char** line cap.
- **Trailing newline** required at EOF.
- **No `any`** — define a proper interface or generic.
- **No `// @ts-ignore`** without a `// why:` comment.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Constant | `UPPER_SNAKE_CASE` | `LOGIN_PATH`, `MAX_RETRY` |
| Type | `PascalCase` | `LayoutType`, `UserInfo` |
| Interface | `PascalCase` (no `I` prefix in v5.7.0) | `UserInfo`, `MenuItem` |
| Component file | `PascalCase.vue` | `VbenModal.vue` |
| Page file | `kebab-case.vue` | `user-profile.vue` |
| Composable | `useCamelCase` exported from `use-<kebab>.ts` | `useScroll` |
| Pinia store | `useXxxStore` | `useUserStore` |
| Helper | camelCase verb-first | `mergeRouteModules` |
| Test spec | `<module>.spec.ts` next to source | `use-scroll.spec.ts` |

## Patterns

### Strict const + literal type

```ts
export const LOGIN_PATH = '/auth/login' as const;
export type LayoutType = 'sidebar-nav' | 'mixed-nav' | 'header-nav';
```

### Composable return type explicit

```ts
export function useScroll(target?: MaybeRefOrGetter<HTMLElement | null>) {
  // ...
  return { y: Ref<number> } as const;
}
```

### Component prop interface colocated

```vue
<script setup lang="ts">
interface Props { title: string; size?: 'small' | 'default' | 'large'; }
const props = withDefaults(defineProps<Props>(), { size: 'default' });
</script>
```

## Pre-commit pipeline

- **OxLint** — fast lint pass
- **OxFmt** — formatter (auto-fixes style)
- **ESLint flat config** — rules OxLint misses
- **Stylelint** — CSS / scoped styles
- **commitlint** — `feat():` / `fix():` / `chore():` etc.
- **vue-tsc** — typecheck (run in CI, not pre-commit)

## Tests

- `vitest` for unit tests, co-located in `__tests__/`.
- `playwright` for E2E (apps only, never in this `@vben-core/form-ui`).
- Test files named `<module>.spec.ts`.

## Forbidden

- ❌ Don't add `lodash` — use `@vben/utils`.
- ❌ Don't inline colors in TS / Vue — read from `useAppTheme()`.
- ❌ Don't disable ESLint rules per-file without a `// why:` comment.
- ❌ Don't commit `.env`, `*.local`, or secrets.
- ❌ Don't import from another component library directly (e.g.
  `naive-ui` outside `shadcn-ui` / `popup-ui` packages).
- ❌ Don't ship `console.log` debug noise — use a logger or remove.
