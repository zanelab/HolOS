
# 填 18 phantom specs 的 2 sub-files

## Goal

之前 `bootstrap-guidelines` 任务给 phantom specs(无 real source code 的 package)写了 **placeholder index.md**:
- `access` / `common-ui` / `composables` / `design` / `form-ui`
- `hooks` / `layout-ui` / `layouts` / `menu-ui` / `popup-ui`
- `shadcn-ui` / `tabs-ui` / `shared` / `typings` / `base` / `@core`
- `plugins` / `request` / `auth` / `common` / `lint-configs-base`
- 等 ~18 个 phantom specs

本次给每个 phantom spec 写真实(基于 vben monorepo 已知约定) **2 sub-files**:
1. **directory-structure.md** — 文件树(预期模式,基于 vben conventions)
2. **component-guidelines.md** — Component/函数使用约定

## 18 phantom targets

按 phantom index.md 中声明的目标:

```
@core / access / base / common-ui / composables / design / form-ui
hooks / layout-ui / layouts / menu-ui / plugins / popup-ui / request
shared / shadcn-ui / tabs-ui / typings
```

## 写每 phantom 的 2 文件

### 1. `directory-structure.md`
- 预期文件树(基于 vben monorepo conventions)
- 关键模式说明
- 标注 "PLACEHOLDER" 段表明这是预期模式,实际不存在源码

### 2. `component-guidelines.md`
- 函数 / Component 使用模式(基于 vue / pinia / vue-router / 等已知约定)
- 至少 1 个 示例代码(synthetic)
- "Forbidden" 段

## Acceptance Criteria

- [ ] **18 phantom specs × 2 文件 = 36 个 .md** 写真实
- [ ] 每文件包含 **明确标 "PLACEHOLDER"** 的开头段
- [ ] 每文件包含 **1 个示例代码**
- [ ] 每文件包含 "Forbidden" 段
- [ ] Commit + push

## Notes

- 幻象 specs **没有真实代码**(phantom package dirs)
- 所有内容基于 **vben monorepo 已知约定** + 类似 package 的模式
- 当真 package 创建时,需替换 placeholder 内容
- 继续 `00-bootstrap-guidelines` 系列 + 之前 fill-phantom 等任务
