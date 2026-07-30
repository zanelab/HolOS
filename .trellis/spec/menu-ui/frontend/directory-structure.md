# menu-ui Directory Structure

**Expected package:** @vben-core/menu-ui — sidebar menu + breadcrumb (planned)

> **PLACEHOLDER DOCS** — 本包 does not exist in the workspace at this time. The expected structure and patterns below are based on `vben v5.7.0` conventions. 替换这些文件 real content when package 添加后.

## 预期目录树

```
@vben/menu-ui/
├── package.json                # workspace name
├── tsconfig.json
└── src/
    ├── index.ts                # public barrel
    └── (one or more module files)
```

## 说明

- This spec directory was auto-created during `bootstrap-guidelines` task
- The expected structure follows `vben v5.7.0` conventions seen in actual packages (`@vben/utils`, `@vben/constants`, etc.)
- See real packages for reference examples

## 禁止

- 不要 create the actual package directory in workspace unless the upstream vben team adds it
- 不要 import from `@vben/menu-ui` — it does not exist