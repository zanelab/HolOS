
# 填 21 个 phantom packages 的 2 子文件

## Goal

之前 `07-29-fill-rest-6-subfiles-batch` 写真实了 **21 真 packages** 的 4 shared sub-files (hook/state/quality/type)。
但 **21 真 packages 的 directory-structure.md + component-guidelines.md** 还没写真实 —— 上一批次只写了 4 sub-files,没写 2 子文件。

本次 task: 完成 **21 真 packages × 2 sub-files = 42 文件** 写真实。

## 21 真 packages 待填 2 子文件

### Apps (5)
- `@vben/backend-mock`
- `@vben/web-antd` - 已写真实 component-guidelines + directory-structure (上一 commit), skip
- `@vben/web-antdv-next`
- `@vben/web-ele`
- `@vben/web-naive`
- `@vben/web-tdesign` - 已写真实, skip
- `@vben/web-holos` - 已写真实, skip

实际上只有 **4 个 web-* apps** (antdv-next / ele / naive / backend-mock) + 已经有的再写真实 **5 apps 的 2 sub-files**

### Internal configs (8)
- `@vben/commitlint-config`
- `@vben/eslint-config`
- `@vben/oxfmt-config`
- `@vben/oxlint-config`
- `@vben/stylelint-config`
- `@vben/tsconfig`
- `@vben/vite-config`

### Lib (8)
- `@vben/constants`
- `@vben/icons`
- `@vben/locales`
- `@vben/preferences`
- `@vben/stores`
- `@vben/styles`
- `@vben/types`
- `@vben/utils`

实际上: **21 真 packages - 3 已写真实 (web-antd/web-tdesign/web-holos) = 18 packages 待填 2 子文件**

## 写每个 package 的 2 sub-files:

### 1. `directory-structure.md`
- 文件树 + 关键模式
- 基于实际 `src/` 目录(读真实代码,不抄 VBen 官方文档)

### 2. `component-guidelines.md` / equivalent
- Vue app: 组件用 vue-3 + UI-framework 模式
- Lib: 函数 / 类型 / Icon 模式,不含 Vue 组件

## Acceptance Criteria

- [x] 18 packages × 2 sub-files = **36 个 `.md`** 写真实
- [x] 每个文件 ≤ 220 行
- [x] 每个文件含 ≥ 1 个 **真实代码示例** 来自该 package source
- [x] 每个文件含 **"Forbidden"** 段
- [x] Commit + push
- [x] 按 Phase 3.4 protocol: 写 commit plan → ok auto (用户前说 ok 自动)

## Notes

- 继续 `00-bootstrap-guidelines` + `07-29-fill-6-subfiles-priority-packages` + `07-29-fill-rest-6-subfiles-batch`
- 18 packages 是 **真 packages**,phantom specs(`access`/`@core` 等) 不动
- index.md(已写真实) + 4 shared sub-files(已写真实)+ 本次 2 sub-files = **完整 7 文件 each 真 package**
