# 跨层思考指南

> **Purpose**: Think through data flow across layers before implementing.

---

## 问题描述

**多数 bug 发生在层与层边界位置**，而不是在层内部。

常见跨层 bug：

- API returns format A, frontend expects format B
- 数据库存储 X，服务转换为 Y但丢失数据
- 多个层以不同方式实现相同逻辑

---

## 实现跨层特性之前

### 第一步：描绘数据流

画出数据是如何流动的：

```
Source → Transform → Store → Retrieve → Transform → Display
```

对每个箭头，问一下：

- 数据是什么格式？
- 可能出现什么问题？
- 谁负责校验？

### 第二步：识别边界

| Boundary              | Common Issues                     |
| --------------------- | --------------------------------- |
| API ↔ Service         | Type mismatches, missing fields   |
| Service ↔ Database    | Format conversions, null handling |
| Backend ↔ Frontend    | Serialization, date formats       |
| Component ↔ Component | Props shape changes               |

### 第三步：定义合同

对每个边界：

- 输入的准确格式是什么？
- 输出的准确格式是什么？
- 可能发生什么错误？

---

## 常见跨层错误

### 错误 1：隐式格式假设

**不好**：不检查就假设日期格式

**推荐**：在边界作明确的格式转换

### 错误 2：散不在各处的校验

**不好**：在多个层中重复校验同一件事

**推荐**：在入口处只校验一次

### 错误 3：泄露的抽象

**不好**：组件知道数据库的表结构

**推荐**：每层只与相邻层交互

### 错误 4：每个消费者都解析相同载荷

**Bad**: A command reads JSONL events and casts fields inline:

```typescript
const thread = (ev as { thread?: string }).thread;
const labels = (ev as { labels?: string[] }).labels;
```

这看上去是本地的，但意味着每个消费者都拥有事件契约的一份私人版本。下次字段变动会只更新某个命令而遗漏另一个。
event contract. The next field change will update one command and miss another.

**推荐**：在事件边界只解码一次，然后导出带类型的折射：

```typescript
if (!isThreadEvent(ev)) return false;
return ev.thread === filter.thread;
```

**Rule**: For append-only logs, JSON streams, RPC payloads, or config files,
为以下内容创建唯一的拥有者：

- event / payload 类型定义
- type guards and normalization from `unknown`
- metadata projections used by UI commands
重放数据源真相中状态的减函数

Rendering code may format fields, but it must not redefine the payload contract.

---

## 跨层特性的检查清单

Before implementation:

- [ ] 已绘制完整数据流向
- [ ] 已识别出所有层边界
- [ ] 已在每个边界定义格式
- [ ] 已决定验证发生的位置

After implementation:

- [ ] 已用极端情况测试（null、空、无效）
- [ ] 已验证每个边界的错误处理
- [ ] 已检查数据能圈中存活
- [ ] 已检查消费者是否引入公共的解码器 / 折射而非
      casting payload fields locally
- [ ] 已检查派生状态是否能指向源事件标识符
      (`seq`, `id`, `version`) instead of inventing a second cursor

---

## 跨平台模板一致性

In Trellis, command templates (e.g., `record-session.md`) exist in **multiple platforms** with identical or near-identical content. This is a cross-layer boundary.

### 检查清单：修改任何命令模板之后

- [ ] Find all platforms with the same command: `find src/templates/*/commands/trellis/ -name "<command>.*"`
- [ ] Update all platform copies (Markdown `.md` and TOML `.toml`)
- [ ] For Gemini TOML: adapt line continuations (`\\` vs `\`) and triple-quoted strings
- [ ] Run `/trellis:check-cross-layer` to verify nothing was missed

**真实-world example**: Updated `record-session.md` in Claude to use `--mode record`, but forgot iFlow, Kilo, OpenCode, and Gemini — caught by cross-layer 检查。

---

## 生成的运行时模板升级一致性

部分生成的文件既是文档又是运行时输入。在 Trellis 中，
`.trellis/workflow.md` is parsed by `get_context.py`, `workflow_phase.py`,
SessionStart filters, and per-turn hooks. Template changes 必须是 validated
同时面对新鲜 init 与升级路径。

### 检查清单：修改运行时解析的模板之后

- [ ] 识别所有读取该模板的运行时解析器，而不仅仅是文件
      writer that installs it
- [ ] 检查相关语法是否位于明显的管理区域之外
      such as tag blocks
- [ ] Verify fresh `init` output and a versioned `update` scenario that writes
      the older `.trellis/.version`
- [ ] 使用一份老版本的完整模板测试例添加一个升级回归，然后
      assert the installed file reaches the current packaged shape
- [ ] 更新拥有该运行时合同的后端规范

---

## 版本化文档边界

Versioned documentation is a cross-layer boundary: source paths, `docs.json`
version routing, and the rendered version selector must all describe the same
release line.

### 检查清单：编辑版本化文档之前

- [ ] Identify the target release line: stable, beta, or RC
- [ ] Verify the edited MDX path matches that line:
  - stable: `docs-site/{start,advanced,...}` and `docs-site/zh/{start,advanced,...}`
  - beta: `docs-site/beta/**` and `docs-site/zh/beta/**`
  - RC: `docs-site/rc/**` and `docs-site/zh/rc/**`
- [ ] Verify `docs.json` navigation points the version label to the same paths
- [ ] 提交前用 grep 查看反侧目录是否含发布线专用术语
- [ ] 将出现在根发布路径下的 beta 内容视为源路径 bug，
      not a rendering bug

**真实-world example**: A beta-only task workflow change documented
`prd.md` + `design.md` + `implement.md`, task-creation consent, and Codex
mode banners under root `start/` and `advanced/` paths. The docs site then
served 0.6 beta behavior under the Release selector. The fix was to restore root
release docs, move the 0.6 content to `beta/` and `zh/beta/`, and add a grep
audit for beta markers against the root release tree.

**真实世界例子**：Codex inline 模式将工作流平台标记从
`[Codex]` / `[Kilo, Antigravity, Windsurf]` to `[codex-sub-agent]` /
`[codex-inline, Kilo, Antigravity, Windsurf]`. Fresh init was correct, but
`trellis update` only merged `[workflow-state:*]` blocks and preserved stale
这些块外的标记。结果：升级后的项目获得了新的 hook 脚本
but old workflow routing, so `get_context.py --mode phase --platform codex`
可能返回空的 Phase 2.1 详情。

---

## 模式探测检查清单

When a CLI auto-detects a mode by probing a remote resource (e.g., checking if `index.json` exists to decide marketplace vs direct download):

### 实现前：

- [ ] Probe runs in **ALL** code paths that 使用 result (interactive, `-y`, `--flag` combos)
- [ ] 区分 404 与临时错误 —— 不要将两者都当作 "未找到"
- [ ] 临时错误 **中断或重试**，永远不要静默切换模式
- [ ] Shared state (caches, prefetched data) is **reset** when context changes (e.g., user switches source)
- [ ] **Shortcut paths** (e.g., `--template` skipping picker) must have the same error-handling quality as the probed path — check that downstream functions don't call catch-all wrappers

### 实现后：

- [ ] 跟踪从探测结果到模式决策分支的每一条路径 —— 不允许 fallthrough
- [ ] External format contracts (giget URI, raw URLs) are tested or at least documented as comments
- [ ] Metadata reads consume a complete response or use a streaming parser — never parse a fixed-size prefix as full JSON
- [ ] When reconstructing a composite identifier from parsed parts, verify **all** fields are included and in the **correct position** (e.g., `provider:repo/path#ref` not `provider:repo#ref/path`)
- [ ] 验证快捷后调用的 **动作函数** 不会内部使用老的 catch-all 取数—— 当需区分错误时必须使用探测质量的变体

**真实-world example**: Custom registry flow had 8 bugs across 3 review rounds: (1) probe only ran in interactive mode, (2) transient errors fell through to wrong mode, (3) giget URI had `#ref` in wrong position, (4) prefetched templates leaked across source switches, (5) `--template` shortcut bypassed probe but `downloadTemplateById` internally used catch-all `fetchTemplateIndex`, turning timeouts into "Template not found".

**真实-world example**: Agent-session update hints fetched npm `latest` metadata with `response.read(4096)` and then parsed it as complete JSON. The `@mindfoldhq/trellis` package metadata exceeded 4 KB, so the JSON was truncated, parse failed silently, and the first session injection showed no update hint. Fix: read the complete response before parsing, and add a regression where `version` is followed by an 8 KB metadata tail.

---

## Cross-Platform Template Consistency

In Trellis, command templates (e.g., `record-session.md`) exist in **multiple platforms** with identical or near-identical content. This is a cross-layer boundary.

### Checklist: After Modifying Any Command Template

- [ ] Find all platforms with the same command: `find src/templates/*/commands/trellis/ -name "<command>.*"`
- [ ] Update all platform copies (Markdown `.md` and TOML `.toml`)
- [ ] For Gemini TOML: adapt line continuations (`\\` vs `\`) and triple-quoted strings
- [ ] Run `/trellis:check-cross-layer` to verify nothing was missed

**真实-world example**: Updated `record-session.md` in Claude to use `--mode record`, but forgot iFlow, Kilo, OpenCode, and Gemini — caught by cross-layer 检查。

---

## Generated Runtime Template Upgrade Consistency

Some generated files are both documentation and runtime input. In Trellis,
`.trellis/workflow.md` is parsed by `get_context.py`, `workflow_phase.py`,
SessionStart filters, and per-turn hooks. Template changes 必须是 validated
against both fresh init and upgrade paths.

### Checklist: After Modifying A Runtime-Parsed Template

- [ ] Identify every runtime parser that reads the template, not just the file
  writer that installs it
- [ ] Check whether relevant syntax lives outside obvious managed regions
  such as tag blocks
- [ ] Verify fresh `init` output and a versioned `update` scenario that writes
  the older `.trellis/.version`
- [ ] Add an upgrade regression using an older pristine template fixture, then
  assert the installed file reaches the current packaged shape
- [ ] Update the backend spec that owns the runtime contract

**真实-world example**: Codex inline mode changed workflow platform markers from
`[Codex]` / `[Kilo, Antigravity, Windsurf]` to `[codex-sub-agent]` /
`[codex-inline, Kilo, Antigravity, Windsurf]`. Fresh init was correct, but
`trellis update` only merged `[workflow-state:*]` blocks and preserved stale
markers outside those blocks. 结果： upgraded projects got new hook scripts
but old workflow routing, so `get_context.py --mode phase --platform codex`
could return empty Phase 2.1 detail.

---

## Mode-Detection Probe Checklist

When a CLI auto-detects a mode by probing a remote resource (e.g., checking if `index.json` exists to decide marketplace vs direct download):

### Before implementing:
- [ ] Probe runs in **ALL** code paths that 使用 result (interactive, `-y`, `--flag` combos)
- [ ] 404 vs transient error are distinguished — don't treat both as "not found"
- [ ] Transient errors **abort or retry**, never silently switch modes
- [ ] Shared state (caches, prefetched data) is **reset** when context changes (e.g., user switches source)
- [ ] **Shortcut paths** (e.g., `--template` skipping picker) must have the same error-handling quality as the probed path — check that downstream functions don't call catch-all wrappers

### After implementing:
- [ ] Trace every path from probe result to the mode-decision branch — no fallthrough
- [ ] External format contracts (giget URI, raw URLs) are tested or at least documented as comments
- [ ] Metadata reads consume a complete response or use a streaming parser — never parse a fixed-size prefix as full JSON
- [ ] When reconstructing a composite identifier from parsed parts, verify **all** fields are included and in the **correct position** (e.g., `provider:repo/path#ref` not `provider:repo#ref/path`)
- [ ] Verify that **action functions** called after a shortcut don't internally 使用 old catch-all fetch — they must 使用 probe-quality variant when error distinction matters

**真实-world example**: Custom registry flow had 8 bugs across 3 review rounds: (1) probe only ran in interactive mode, (2) transient errors fell through to wrong mode, (3) giget URI had `#ref` in wrong position, (4) prefetched templates leaked across source switches, (5) `--template` shortcut bypassed probe but `downloadTemplateById` internally used catch-all `fetchTemplateIndex`, turning timeouts into "Template not found".

**真实-world example**: Agent-session update hints fetched npm `latest` metadata with `response.read(4096)` and then parsed it as complete JSON. The `@mindfoldhq/trellis` package metadata exceeded 4 KB, so the JSON was truncated, parse failed silently, and the first session injection showed no update hint. Fix: read the complete response before parsing, and add a regression where `version` is followed by an 8 KB metadata tail.

---

## 何时创建流程文档

Create detailed flow docs when:

- 功能跨越 3 个以上层
- 涉及多个团队
- 数据格式复杂
- 该功能以往引起过 bug

---

## 事件日志 / 投影边界

Append-only logs are cross-layer contracts. A single event travels through:

```
CLI input → event writer → events.jsonl → reader → filter → reducer → display
```

### 检查清单：添加新的事件类型或字段之后

- [ ] 将该事件类型加入中央事件分类系统
- [ ] 在事件层增加带类型的事件变体或类型卫具
- [ ] 为来自的数组/对象字段增加归一化辅助函数
      user input or JSON
- [ ] Keep `seq` / `id` assignment in the event writer only
- [ ] 让过滤器与减函数消费带类型的事件卫具，而非局部强转
- [ ] Make display code consume reducer output or typed events, not raw JSON
- [ ] 至少添加一个验证历史重放与实时过滤的回归测试
      使用 same filter model

**真实-world example**: Thread channels added `kind: "thread"`, `description`,
`context`, labels, and `lastSeq`. The first implementation replayed thread
state correctly, but several commands still re-parsed event payload fields with
local casts. The fix was to make the core event layer own `ThreadChannelEvent`
and `isThreadEvent`, make `reduceChannelMetadata` the only channel metadata
projection, and make `reduceThreads` the only thread replay reducer.
