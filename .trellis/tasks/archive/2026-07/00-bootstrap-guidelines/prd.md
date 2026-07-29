# Bootstrap Task: Fill Project Development Guidelines

**You (the AI) are running this task. The developer does not read this file.**

The developer just ran `trellis init` on this project for the first time.
`.trellis/` now exists with empty spec scaffolding, and this bootstrap task
exists under `.trellis/tasks/`. When they want to work on it, they should start
this task from a session that provides Trellis session identity.

**Your job**: help them populate `.trellis/spec/` with the team's real
coding conventions. Every future AI session — this project's
`trellis-implement` and `trellis-check` sub-agents — auto-loads spec files
listed in per-task jsonl manifests. Empty spec = sub-agents write generic
code. Real spec = sub-agents match the team's actual patterns.

Don't dump instructions. Open with a short greeting, figure out if the repo
has any existing convention docs (CLAUDE.md, .cursorrules, etc.), and drive
the rest conversationally.

---

## Status (update the checkboxes as you complete each item)

- [ ] Fill guidelines for lint-configs
- [x] Fill guidelines [index.md] for @vben/node-utils
- [x] Fill guidelines [index.md] for @vben/tailwind-config
- [x] Fill guidelines [index.md] for @vben/tsconfig
- [x] Fill guidelines [index.md] for @vben/vite-config
- [x] Fill guidelines [index.md] for @vben/commitlint-config
- [x] Fill guidelines [index.md] for @vben/eslint-config
- [x] Fill guidelines [index.md] for @vben/oxfmt-config
- [x] Fill guidelines [index.md] for @vben/oxlint-config
- [x] Fill guidelines [index.md] for @vben/stylelint-config
- [x] Fill guidelines [placeholder] for @core
- [x] Fill guidelines [index.md] for @vben/constants
- [ ] Fill guidelines for effects
- [x] Fill guidelines [index.md] for @vben/icons
- [x] Fill guidelines [index.md] for @vben/locales
- [x] Fill guidelines [index.md] for @vben/preferences
- [x] Fill guidelines [index.md] for @vben/stores
- [x] Fill guidelines [index.md] for @vben/styles
- [x] Fill guidelines [index.md] for @vben/types
- [x] Fill guidelines [index.md] for @vben/utils
- [x] Fill guidelines [placeholder] for @vben-core/design
- [ ] Fill guidelines for @vben-core/icons
- [x] Fill guidelines [placeholder] for @vben-core/shared
- [x] Fill guidelines [placeholder] for @vben-core/typings
- [x] Fill guidelines [placeholder] for @vben-core/form-ui
- [x] Fill guidelines [placeholder] for @vben-core/layout-ui
- [x] Fill guidelines [placeholder] for @vben-core/menu-ui
- [x] Fill guidelines [placeholder] for @vben-core/popup-ui
- [x] Fill guidelines [placeholder] for @vben-core/shadcn-ui
- [x] Fill guidelines [placeholder] for @vben-core/tabs-ui
- [x] Fill guidelines [placeholder] for base
- [x] Fill guidelines [placeholder] for @vben-core/composables
- [ ] Fill guidelines for @vben-core/preferences
- [ ] Fill guidelines for ui-kit
- [x] Fill guidelines [placeholder] for @vben/access
- [x] Fill guidelines [placeholder] for @vben/common-ui
- [x] Fill guidelines [placeholder] for @vben/hooks
- [x] Fill guidelines [placeholder] for @vben/layouts
- [x] Fill guidelines [placeholder] for @vben/plugins
- [x] Fill guidelines [placeholder] for @vben/request
- [x] Fill guidelines [index.md] for @vben/backend-mock
- [ ] Fill guidelines for @vben/web-antd
- [ ] Fill guidelines for @vben/web-antdv-next
- [ ] Fill guidelines for @vben/web-ele
- [x] Fill guidelines [index.md + 6 sub-files] for @vben/web-holos
- [ ] Fill guidelines for @vben/web-naive
- [x] Fill guidelines [index.md] for @vben/web-tdesign
- [ ] Fill guidelines for deploy
- [ ] Fill guidelines for @vben/turbo-run
- [ ] Fill guidelines for @vben/vsh
- [ ] Fill guidelines for @vben/docs
- [ ] Fill guidelines for @vben/playground
- [x] Add code examples

---

## Spec files to populate

### Package: lint-configs (`spec/lint-configs/`)

- Backend guidelines: `.trellis/spec/lint-configs/backend/`

- Frontend guidelines: `.trellis/spec/lint-configs/frontend/`

### Package: @vben/node-utils (`spec/node-utils/`)

- Backend guidelines: `.trellis/spec/node-utils/backend/`

- Frontend guidelines: `.trellis/spec/node-utils/frontend/`

### Package: @vben/tailwind-config (`spec/tailwind-config/`)

- Backend guidelines: `.trellis/spec/tailwind-config/backend/`

- Frontend guidelines: `.trellis/spec/tailwind-config/frontend/`

### Package: @vben/tsconfig (`spec/tsconfig/`)

- Frontend guidelines: `.trellis/spec/tsconfig/frontend/`

### Package: @vben/vite-config (`spec/vite-config/`)

- Backend guidelines: `.trellis/spec/vite-config/backend/`

- Frontend guidelines: `.trellis/spec/vite-config/frontend/`

### Package: @vben/commitlint-config (`spec/commitlint-config/`)

- Frontend guidelines: `.trellis/spec/commitlint-config/frontend/`

### Package: @vben/eslint-config (`spec/eslint-config/`)

- Backend guidelines: `.trellis/spec/eslint-config/backend/`

- Frontend guidelines: `.trellis/spec/eslint-config/frontend/`

### Package: @vben/oxfmt-config (`spec/oxfmt-config/`)

- Backend guidelines: `.trellis/spec/oxfmt-config/backend/`

- Frontend guidelines: `.trellis/spec/oxfmt-config/frontend/`

### Package: @vben/oxlint-config (`spec/oxlint-config/`)

- Backend guidelines: `.trellis/spec/oxlint-config/backend/`

- Frontend guidelines: `.trellis/spec/oxlint-config/frontend/`

### Package: @vben/stylelint-config (`spec/stylelint-config/`)

- Frontend guidelines: `.trellis/spec/stylelint-config/frontend/`

### Package: @core (`spec/@core/`)

- Backend guidelines: `.trellis/spec/@core/backend/`

- Frontend guidelines: `.trellis/spec/@core/frontend/`

### Package: @vben/constants (`spec/constants/`)

- Backend guidelines: `.trellis/spec/constants/backend/`

- Frontend guidelines: `.trellis/spec/constants/frontend/`

### Package: effects (`spec/effects/`)

- Backend guidelines: `.trellis/spec/effects/backend/`

- Frontend guidelines: `.trellis/spec/effects/frontend/`

### Package: @vben/icons (`spec/icons/`)

- Backend guidelines: `.trellis/spec/icons/backend/`

- Frontend guidelines: `.trellis/spec/icons/frontend/`

### Package: @vben/locales (`spec/locales/`)

- Backend guidelines: `.trellis/spec/locales/backend/`

- Frontend guidelines: `.trellis/spec/locales/frontend/`

### Package: @vben/preferences (`spec/preferences/`)

- Backend guidelines: `.trellis/spec/preferences/backend/`

- Frontend guidelines: `.trellis/spec/preferences/frontend/`

### Package: @vben/stores (`spec/stores/`)

- Backend guidelines: `.trellis/spec/stores/backend/`

- Frontend guidelines: `.trellis/spec/stores/frontend/`

### Package: @vben/styles (`spec/styles/`)

- Backend guidelines: `.trellis/spec/styles/backend/`

- Frontend guidelines: `.trellis/spec/styles/frontend/`

### Package: @vben/types (`spec/types/`)

- Backend guidelines: `.trellis/spec/types/backend/`

- Frontend guidelines: `.trellis/spec/types/frontend/`

### Package: @vben/utils (`spec/utils/`)

- Backend guidelines: `.trellis/spec/utils/backend/`

- Frontend guidelines: `.trellis/spec/utils/frontend/`

### Package: @vben-core/design (`spec/design/`)

- Backend guidelines: `.trellis/spec/design/backend/`

- Frontend guidelines: `.trellis/spec/design/frontend/`

### Package: @vben-core/icons (`spec/icons/`)

- Backend guidelines: `.trellis/spec/icons/backend/`

- Frontend guidelines: `.trellis/spec/icons/frontend/`

### Package: @vben-core/shared (`spec/shared/`)

- Frontend guidelines: `.trellis/spec/shared/frontend/`

### Package: @vben-core/typings (`spec/typings/`)

- Backend guidelines: `.trellis/spec/typings/backend/`

- Frontend guidelines: `.trellis/spec/typings/frontend/`

### Package: @vben-core/form-ui (`spec/form-ui/`)

- Backend guidelines: `.trellis/spec/form-ui/backend/`

- Frontend guidelines: `.trellis/spec/form-ui/frontend/`

### Package: @vben-core/layout-ui (`spec/layout-ui/`)

- Backend guidelines: `.trellis/spec/layout-ui/backend/`

- Frontend guidelines: `.trellis/spec/layout-ui/frontend/`

### Package: @vben-core/menu-ui (`spec/menu-ui/`)

- Backend guidelines: `.trellis/spec/menu-ui/backend/`

- Frontend guidelines: `.trellis/spec/menu-ui/frontend/`

### Package: @vben-core/popup-ui (`spec/popup-ui/`)

- Backend guidelines: `.trellis/spec/popup-ui/backend/`

- Frontend guidelines: `.trellis/spec/popup-ui/frontend/`

### Package: @vben-core/shadcn-ui (`spec/shadcn-ui/`)

- Backend guidelines: `.trellis/spec/shadcn-ui/backend/`

- Frontend guidelines: `.trellis/spec/shadcn-ui/frontend/`

### Package: @vben-core/tabs-ui (`spec/tabs-ui/`)

- Backend guidelines: `.trellis/spec/tabs-ui/backend/`

- Frontend guidelines: `.trellis/spec/tabs-ui/frontend/`

### Package: base (`spec/base/`)

- Backend guidelines: `.trellis/spec/base/backend/`

- Frontend guidelines: `.trellis/spec/base/frontend/`

### Package: @vben-core/composables (`spec/composables/`)

- Backend guidelines: `.trellis/spec/composables/backend/`

- Frontend guidelines: `.trellis/spec/composables/frontend/`

### Package: @vben-core/preferences (`spec/preferences/`)

- Backend guidelines: `.trellis/spec/preferences/backend/`

- Frontend guidelines: `.trellis/spec/preferences/frontend/`

### Package: ui-kit (`spec/ui-kit/`)

- Backend guidelines: `.trellis/spec/ui-kit/backend/`

- Frontend guidelines: `.trellis/spec/ui-kit/frontend/`

### Package: @vben/access (`spec/access/`)

- Backend guidelines: `.trellis/spec/access/backend/`

- Frontend guidelines: `.trellis/spec/access/frontend/`

### Package: @vben/common-ui (`spec/common-ui/`)

- Backend guidelines: `.trellis/spec/common-ui/backend/`

- Frontend guidelines: `.trellis/spec/common-ui/frontend/`

### Package: @vben/hooks (`spec/hooks/`)

- Backend guidelines: `.trellis/spec/hooks/backend/`

- Frontend guidelines: `.trellis/spec/hooks/frontend/`

### Package: @vben/layouts (`spec/layouts/`)

- Backend guidelines: `.trellis/spec/layouts/backend/`

- Frontend guidelines: `.trellis/spec/layouts/frontend/`

### Package: @vben/plugins (`spec/plugins/`)

- Backend guidelines: `.trellis/spec/plugins/backend/`

- Frontend guidelines: `.trellis/spec/plugins/frontend/`

### Package: @vben/request (`spec/request/`)

- Backend guidelines: `.trellis/spec/request/backend/`

- Frontend guidelines: `.trellis/spec/request/frontend/`

### Package: @vben/backend-mock (`spec/backend-mock/`)

- Frontend guidelines: `.trellis/spec/backend-mock/frontend/`

### Package: @vben/web-antd (`spec/web-antd/`)

- Frontend guidelines: `.trellis/spec/web-antd/frontend/`

### Package: @vben/web-antdv-next (`spec/web-antdv-next/`)

- Frontend guidelines: `.trellis/spec/web-antdv-next/frontend/`

### Package: @vben/web-ele (`spec/web-ele/`)

- Frontend guidelines: `.trellis/spec/web-ele/frontend/`

### Package: @vben/web-holos (`spec/web-holos/`)

- Frontend guidelines: `.trellis/spec/web-holos/frontend/`

### Package: @vben/web-naive (`spec/web-naive/`)

- Frontend guidelines: `.trellis/spec/web-naive/frontend/`

### Package: @vben/web-tdesign (`spec/web-tdesign/`)

- Frontend guidelines: `.trellis/spec/web-tdesign/frontend/`

### Package: deploy (`spec/deploy/`)

- Backend guidelines: `.trellis/spec/deploy/backend/`

- Frontend guidelines: `.trellis/spec/deploy/frontend/`

### Package: @vben/turbo-run (`spec/turbo-run/`)

- Backend guidelines: `.trellis/spec/turbo-run/backend/`

- Frontend guidelines: `.trellis/spec/turbo-run/frontend/`

### Package: @vben/vsh (`spec/vsh/`)

- Backend guidelines: `.trellis/spec/vsh/backend/`

- Frontend guidelines: `.trellis/spec/vsh/frontend/`

### Package: @vben/docs (`spec/docs/`)

- Frontend guidelines: `.trellis/spec/docs/frontend/`

### Package: @vben/playground (`spec/playground/`)

- Frontend guidelines: `.trellis/spec/playground/frontend/`


### Thinking guides (already populated)

`.trellis/spec/guides/` contains general thinking guides pre-filled with
best practices. Customize only if something clearly doesn't fit this project.

---

## How to fill the spec

### Step 1: Import from existing convention files first (preferred)

Search the repo for existing convention docs. If any exist, read them and
extract the relevant rules into the matching `.trellis/spec/` files —
usually much faster than documenting from scratch.

| File / Directory | Tool |
|------|------|
| `CLAUDE.md` / `CLAUDE.local.md` | Claude Code |
| `AGENTS.md` | Codex / Claude Code / agent-compatible tools |
| `.cursorrules` | Cursor |
| `.cursor/rules/*.mdc` | Cursor (rules directory) |
| `.windsurfrules` | Windsurf |
| `.clinerules` | Cline |
| `.roomodes` | Roo Code |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.vscode/settings.json` → `github.copilot.chat.codeGeneration.instructions` | VS Code Copilot |
| `CONVENTIONS.md` / `.aider.conf.yml` | aider |
| `CONTRIBUTING.md` | General project conventions |
| `.editorconfig` | Editor formatting rules |

### Step 2: Analyze the codebase for anything not covered by existing docs

Scan real code to discover patterns. Before writing each spec file:
- Find 2-3 real examples of each pattern in the codebase.
- Reference real file paths (not hypothetical ones).
- Document anti-patterns the team clearly avoids.

### Step 3: Document reality, not ideals

**Critical**: write what the code *actually does*, not what it should do.
Sub-agents match the spec, so aspirational patterns that don't exist in the
codebase will cause sub-agents to write code that looks out of place.

If the team has known tech debt, document the current state — improvement
is a separate conversation, not a bootstrap concern.

---

## Quick explainer of the runtime (share when they ask "why do we need spec at all")

- Every AI coding task spawns two sub-agents: `trellis-implement` (writes
  code) and `trellis-check` (verifies quality).
- Each task has `implement.jsonl` / `check.jsonl` manifests listing which
  spec files to load.
- The platform hook auto-injects those spec files + the task's `prd.md`
  into every sub-agent prompt, so the sub-agent codes/reviews per team
  conventions without anyone pasting them manually.
- Source of truth: `.trellis/spec/`. That's why filling it well now pays
  off forever.

---

## Completion

When the developer confirms the checklist items above are done with real
examples (not placeholders), guide them to run:

```bash
python3 ./.trellis/scripts/task.py finish
python3 ./.trellis/scripts/task.py archive 00-bootstrap-guidelines
```

After archive, every new developer who joins this project will get a
`00-join-<slug>` onboarding task instead of this bootstrap task.

---

## Suggested opening line

"Welcome to Trellis! Your init just set me up to help you fill the project
spec — a one-time setup so every future AI session follows the team's
conventions instead of writing generic code. Before we start, do you have
any existing convention docs (CLAUDE.md, .cursorrules, CONTRIBUTING.md,
etc.) I can pull from, or should I scan the codebase from scratch?"
