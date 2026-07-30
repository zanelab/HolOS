# design Directory Structure

**Expected package:** @vben-core/design — design tokens (planned)

> **PLACEHOLDER DOCS** — This package does not exist in the workspace at this time. The expected structure and patterns below are based on `vben v5.7.0` conventions. Replace these files with real content when the package is added.

## Expected Tree

```
@vben/design/
├── package.json                # workspace name
├── tsconfig.json
└── src/
    ├── index.ts                # public barrel
    └── (one or more module files)
```

## Notes

- This spec directory was auto-created during `bootstrap-guidelines` task
- The expected structure follows `vben v5.7.0` conventions seen in actual packages (`@vben/utils`, `@vben/constants`, etc.)
- See real packages for reference examples

## Forbidden

- Do not create the actual package directory in workspace unless the upstream vben team adds it
- Do not import from `@vben/design` — it does not exist