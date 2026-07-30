
# 填 18 phantom specs 的 4 sub-files

## Goal

之前 `fill-phantom-docs-best-guess` task 写真实了 18 phantom specs 的 2 子文件(directory-structure + component-guidelines)。

本次: 完成**剩余 4 子文件** 写真实:
- `hook-guidelines.md`
- `state-management.md`
- `quality-guidelines.md`
- `type-safety.md`

= 18 phantom specs × 4 files = **72 .md 文件**

## 18 phantom targets

跟之前 task 一样:
```
@core / access / base / common-ui / composables / design / form-ui
hooks / layout-ui / layouts / menu-ui / plugins / popup-ui / request
shared / shadcn-ui / tabs-ui / typings
```

## 每 phantom 写真实 4 文件

### 1. `hook-guidelines.md`
- Vue apps: useXxx composables, use VbenDefault Patterns
- Libs: No Vue hooks + wrap in app composables pattern
- 注: phantom packages 注明 "PLACEHOLDER"

### 2. `state-management.md`
- Apps: Pinia stores + preferences 决策树
- Libs: stateless helpers + no Pinia
- 注: 适用于 phantom state model

### 3. `quality-guidelines.md`
- TS strict mode + 4-space + OxLint + ESLint + commitlint
- naming conventions + Pre-commit hooks
- 注: 适用 vben v5.7.0 standards

### 4. `type-safety.md`
- Strict mode TS via @vben/tsconfig
- Required patterns (RouteRecordRaw, Props, types)
- Forbidden (no any, no `as` cast)

## Acceptance Criteria

- [x] **18 phantom × 4 files = 72 .md** 写真实
- [x] 每文件含 **"PLACEHOLDER DOCS"** banner(标 no real source)
- [x] 每文件含 1 个 synthetic 代码示例
- [x] 每文件含 **"Forbidden"** 段
- [x] Commit + push
- [x] 按 Phase 3.4 protocol: 写 commit plan → ok auto(用户前说 ok 自动)

## Notes

- 完成 5-task phantom docs 系列最后一批
- 此时 18 phantom specs 全部 7 docs 各写真实
- 18 phantom × 7 = 126 placeholder .md files 总计
</content>
