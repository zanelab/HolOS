
# 填剩余 21 个 packages 的 6 子文件

## Goal

写真实 **21 个 packages × 6 子文件 = 126 `.md` 文件**。之前 task (`07-29-fill-6-subfiles-priority-packages`) 完成 3 packages 写真实。这次覆盖 **剩余所有 写真实 packages in workspace**:

### 写真实 packages (21 个)

**Apps (6)**
- `@vben/backend-mock` — Nitro mock server at `apps/backend-mock/`
- `@vben/web-antd` — Ant Design Vue flavor
- `@vben/web-antdv-next` — Ant Design Vue Next flavor
- `@vben/web-ele` — Element Plus flavor
- `@vben/web-naive` — Naive UI flavor

**Internal config (8)**
- `@vben/tsconfig` — base tsconfig
- `@vben/vite-config` — vite + plugins
- `@vben/commitlint-config` — commit lint
- `@vben/eslint-config` — ESLint flat config
- `@vben/oxfmt-config` — OxFmt config
- `@vben/oxlint-config` — OxLint config
- `@vben/stylelint-config` — stylelint config

**Packages (7)**
- `@vben/constants` — shared constants + types
- `@vben/icons` — iconify + svg components
- `@vben/locales` — i18n setup + langs
- `@vben/preferences` — app config
- `@vben/stores` — Pinia stores
- `@vben/styles` — design system CSS
- `@vben/types` — shared types
- `@vben/utils` — utilities (mergeRouteModules, etc.)

### NOT included (phantom specs in Trellis init)

`access / common-ui / composables / design / form-ui / hooks / layout-ui / layouts / menu-ui / popup-ui / shared / shadcn-ui / tabs-ui / typings / base / @core / plugins / request / auth / common / lint-configs/base / lint-configs/stylelint-config / etc` — these **don't have corresponding packages** in workspace. Already have placeholder index.md from prior task.

## Per-Package Requirements

For each package, photo-write **6 sub-files** in `.trellis/spec/<pkg>/frontend/`:

1. **`directory-structure.md`** — actual tree + key file roles
2. **`component-guidelines.md`** — for Vue apps: component patterns; for libs: function/helper patterns
3. **`hook-guidelines.md`** — when applicable; for libs without hooks → "Component" / utility patterns
4. **`state-management.md`** — Vue apps: store + composable patterns; libs: stateless helpers patterns
5. **`quality-guidelines.md`** — lint / commitlint / naming / TypeScript strict
6. **`type-safety.md`** — TypeScript / Vue type patterns from actual code

All content **based on real source code** in `/opt/data/workspace/holos/<path>` — read before write.

## Acceptance Criteria

- [x] **126** `.md` files written across 21 packages
- [x] Each file ≤ 220 lines; **no placeholder text**
- [x] Each file contains ≥ 1 **real code snippet** from actual source
- [x] Each file contains **"Forbidden"** section
- [x] Commits: **per-package batches** (so each commit is logical and revertible)
- [x] Push to origin
- [x] **Per Phase 3.4 protocol**: present plan → ask confirmation per batch
- [x] Archive task after completion

## Notes

- Continues `00-bootstrap-guidelines` + `07-29-fill-6-subfiles-priority-packages`
- **Phantom specs** (no real package) **not touched** — placeholder index.md from previous task suffices
- index.md already written for all 21 packages (from bootstrap task) — **don't rewrite**
</content>
