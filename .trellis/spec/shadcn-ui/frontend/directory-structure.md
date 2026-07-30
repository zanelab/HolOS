# shadcn-ui — PLACEHOLDER SPEC

**Expected package:** `@vben-core/shadcn-ui` — shadcn-vue primitives wrapped with `Vben` prefix — `VbenButton`, `VbenInput`, `VbenSelect`, `VbenCheckbox`, `VbenDialog`. Re-skinned, re-exported, themeable.

> ⚠️ **PLACEHOLDER DOCS** — This package does **not** exist in the current
> workspace. The structure, conventions, and code examples below are
> best-guess projections based on the upstream `vben v5.7.0` monorepo
> (`vbenjs/vben-admin-monorepo`) and the role this package plays
> in a real vben app. **Replace this file with real content when (and
> only when) the corresponding `packages/shadcn-ui/`
> directory lands upstream.**

Do **not** implement against this placeholder — code that imports from
`@vben-core/shadcn-ui` will fail to typecheck.
## Expected directory tree (vben v5.7.0 conventions)

```
@vben-core/shadcn-ui/
├── package.json                        # name "@vben-core/shadcn-ui" v5.7.0
├── tsconfig.json                       # extends @vben/tsconfig/library.json
├── README.md                           # (optional) usage example
└── src/
    ├── index.ts                        # 公开 barrel — re-exports public API
    └── (one or more module files)
```

### Typical src/ layout (varies by role — `shadcn`)

```
src/
├── index.ts
├── core.ts                            # main entry helpers
├── types.ts                           # public TS types
├── constants.ts                       # (when role needs runtime constants)
├── helpers/                           # per-feature helper groups
│   ├── index.ts
│   ├── has-access.ts                  # example per role
│   └── generate-accessible.ts
├── components/                        # (UI role only — see component-guidelines.md)
│   └── <PascalCase>.vue
└── __tests__/                         # co-located unit tests
    └── helpers.spec.ts
```

## Per-role layout hints

| Role (shadcn) | Extra dirs expected |
|---|---|
| composite | `src/<group>/...` mirroring sub-packages |
| acl | `src/has-access.ts`, `src/generate-accessible.ts`, `src/types.ts` |
| ui-primitives | `src/components/<PascalCase>.vue` |
| fallback-pages | `src/about/`, `src/profile/`, `src/authentication/` |
| composables | `src/use-<feature>.ts` per hook |
| tokens | `src/tokens.css`, `src/preset.ts` |
| form | `src/components/form/`, `src/components/form-item/`, `src/form-api.ts` |
| app-hooks | `src/use-app-<feature>.ts` |
| layout-primitives | `src/components/layout-<region>/` |
| layouts | `src/basic-layout/`, `src/auth-layout/`, `src/i-frame-view/`, `src/blank-layout/` |
| menu | `src/components/menu/`, `src/components/breadcrumb/` |
| vite-plugins | `src/vite/<name>.ts` per plugin |
| popups | `src/components/modal/`, `src/components/drawer/`, `src/components/dropdown/` |
| http | `src/request-client.ts`, `src/interceptors/`, `src/helpers/` |
| runtime-constants | `src/error-codes.ts`, `src/timeouts.ts` |
| shadcn | `src/components/<kebab>/<PascalCase>.vue` |
| tabs | `src/components/tabs-view/`, `src/components/tab-button/`, `src/context-menu.ts` |
| typings | `src/<group>.ts` (e.g. `record.ts`, `partial.ts`) |

## Patterns

- **Public barrel** — `src/index.ts` is the **only** import entry point.
  Deep imports like `@vben-core/shadcn-ui/internal/x` are forbidden.
- **Co-located tests** — vitest specs live in `__tests__/` next to source.
- **Each subdirectory** owns its own `index.ts` to keep tree-shaking tight.

## Forbidden

- ❌ Don't `import` from `@vben-core/shadcn-ui/internal/*` — only the public barrel.
- ❌ Don't create the actual `packages/shadcn-ui/`
  directory in this workspace — it's upstream-owned.
- ❌ Don't ship a `dist/` or `lib/` folder in the placeholder spec.
- ❌ Don't add `package.json` here — spec dir is docs, not buildable.
- ❌ Don't reference node_modules paths; everything is workspace alias.
