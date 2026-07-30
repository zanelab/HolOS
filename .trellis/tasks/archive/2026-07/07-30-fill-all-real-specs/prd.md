
# 写真实 134 stub spec .md files (真正写真实,不剩 generic placeholders)

## 现状 (audit 2026-07-30)

```
=== spec files by line count ===
134 个 stub (<30 lines)
444 个 short (30-100 lines)
0 medium (100-200 lines)
2 long (200+)
Total: 580 files
平均 41 lines/file
```

**Issue**: 之前的"写真实" pass 写了 generic placeholder content (e.g.
"## Conventions\n- Don't use any\n- Don't add ts-ignore"). 这是 template 级别 not real content.
虽然 canonical-pattern 文件(如 web-holos / web-tdesign / node-utils /
tailwind-config)之前已 写真实 ~140 行 + 示例,大多数 specs 还停在
20-30 行 stub。

**User feedback**: "我发现 .trellis/spec 下每个目录下的规格都是未填写状态,
请根据 trellis 流程规划所有需要填写的文档,按要求完成文档的填写"

## Target

写真实 **所有 134 stub files**,每个 ≥ 80 行 有内容:
- directory-structure.md
- component-guidelines.md
- hook-guidelines.md
- state-management.md
- quality-guidelines.md
- type-safety.md

每文件含:
- 文件 purpose
- 真实 Vue/Pinia/Composables/CSS/TypeScript 模式(基于 vben v5.7.0 conventions)
- 至少 1 个 真实 code 示例 (generic but accurate v5.7.0 patterns)
- "Forbidden" 段 (不干的事)
- 参考信息

## 写真实的 packages(优先)

### Phase 1 - 真 packages(已有 source code)
1. **apps/backend-mock** - Nitro mock server (需写真实 detail)
2. **packages/constants** - 真实 constants + types
3. **packages/icons** - Iconify + SvgXxx
4. **packages/locales** - i18n JSON + 模块
5. **packages/preferences** - defineOverridesPreferences
6. **packages/stores** - Pinia setup stores
7. **packages/styles** - per-framework CSS
8. **packages/types** - shared types
9. **packages/utils** - helper functions
10. **internal/tsconfig** - shared tsconfig
11. **internal/vite-config** - vite plugins + config
12. **internal/commitlint-config** - commit rules
13. **internal/eslint-config** - ESLint flat config
14. **internal/oxfmt-config** - OxFmt config
15. **internal/oxlint-config** - OxLint config
16. **internal/stylelint-config** - stylelint config
17. **internal/lint-configs** - aggregate

### Phase 2 - Phantom specs (no source - use v5.7.0 conventions)
18. **@core / access / base / common-ui / composables / design**
19. **form-ui / hooks / layout-ui / layouts / menu-ui**
20. **popup-ui / plugins / request / shared / shadcn-ui**
21. **tabs-ui / typings**

## Strategy

每个 file **target 80-150 行** 包括:
- ## Overview (项目用途)
- ## Conventions (基于 vben v5.7.0 实际代码模式)
- ## Real Example (来自 vben source / or generic working pattern)
- ## Anti-Patterns / Forbidden
- ## Related resources

**禁止 generic placeholder text**。每个文件要有 actionable content。

## Acceptance Criteria

- [ ] 134 stub files 写真实 (≥80 lines each)
- [ ] 总_lines 增加 (~10K) 
- [ ] All files have real code example + Forbidden section
- [ ] Commit + push

## Notes

- Trellis batch-specs.py already writes 4 sub-files per package kind
- These need to be rewritten with FULL content (not generic 6-line stubs)
- Will batch by package kind + read source code references for accuracy
