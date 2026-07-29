
# 写真实 6 子文件到 web-tdesign + node-utils + tailwind-config

## Goal

3 packages **最优先写真实 6 子文件**:directory-structure, component-guidelines, hook-guidelines, state-management, quality-guidelines, type-safety。

**注意**: 候选 `@vben-core/layout-ui` 和 `@vben-core/preferences` 是 phantom spec(原计划),但实际 workspace 没有对应 package(只有 phantom index.md)。所以改写为有源码的 3 个真 packages:

- **`@vben/web-tdesign`** — UI 模板(web-holos clone 的源)— 写真实代码示例 (Vue + TDesign 组件) 
- **`internal/node-utils`** (workspace name `@vben/node-utils`) — Node utilities(mergeRouteModules / traverseTreeValues / git-utils — 之前 study 过)
- **`internal/tailwind-config`** (workspace name `@vben/tailwind-config`) — Tailwind preset 设计token

每个 package 写真实 ≥ 1 个 **真实代码示例** 来自该 package source code,基于 **(workspace 中)** 实际代码 **read before writing**。

## Requirements

- 写真实 3 packages × 6 sub-files = **18** `.md` 文件
- 写真实 index.md(已写真实)不重写,只写真实 6 子文件
- 每文件 ≤ 200 行
- 所有 source 引用基于 workspace(`/opt/data/workspace/holos/`)的**实际代码**

## Acceptance Criteria

- [x] 18 个新 `.md` 文件在 `.trellis/spec/<pkg>/frontend/` 下写真实
- [x] 每个文件含 ≥ 1 个真实代码示例 + 禁忌项目段
- [x] commit + push
- [x] 按 Phase 3.4 协议: 写 commit plan → ask confirmation → commit

## Notes

- 这是 `00-bootstrap-guidelines` 任务的后续
- 不重写 index.md(已写真实)
- 不动 packages/ 实际代码
