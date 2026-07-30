# base Directory Structure

**Expected package:** @vben-core/base — global types and shared interfaces (planned)

> **PLACEHOLDER DOCS** — 本包 does not exist in the workspace at this time. The expected structure and patterns below are based on `vben v5.7.0` conventions. 替换这些文件 real content when package 添加后.

## 预期目录树

```
@vben/ase/
├── package.json                # workspace name
├── tsconfig.json
└── src/
    ├── index.ts                # public barrel
    └── (one or more module files)
```

## 说明

- This spec directory was auto-created during `bootstrap-guidelines` task
- The expected structure follows `vben v5.7.0` conventions seen in actual packages (`@vben/utils`, `@vben/constants`, etc.)
- 参考真实 package 的示例

## 禁止

- 除非上游 vben 团队添加，否则不要在工作区中创建实际的 package 目录
- 不要 import from `@vben/ase` — it does not exist