# 代码复用思考指南

> **Purpose**: Stop and think before creating new code - does it already exist?

---

## 问题描述

**重复代码是不一致 bug 的第一大源头。**

当你复制粘贴或重写已有逻辑时：
- bug 修复无法传播
- 随着时间变化，行为变异
- 代码库越来越难以理解

---

## 写新代码之前

### 第一步：先搜索

```bash
# Search for similar function names
grep -r "functionName" .

# Search for similar logic
grep -r "keyword" .
```

### 第二步：提出这些问题

| Question | If Yes... |
|----------|-----------|
| Does a similar function exist? | Use or extend it |
| Is this pattern used elsewhere? | Follow the existing pattern |
| Could this be a shared utility? | Create it in the right place |
| Am I copying code from another file? | **STOP** - extract to shared |

---

## 常见重复模式

### 模式 1：复制粘贴函数

**不好**：将校验函数复制到另一个文件

**推荐**：抽取为共享工具函数，在需要处 import

### 模式 2：相似组件

**不好**：创建一个与存量组件 80% 重叠的新组件

**推荐**：以 props / 变体扩展现有组件

### 模式 3：重复的常量

**不好**：在多个文件定义同一个常量

**推荐**：唯一准确源，处处 import

### 模式 4：重复的载荷字段提取

**Bad**: Multiple consumers cast the same JSON/event fields locally:

```typescript
const description = (ev as { description?: string }).description;
const context = (ev as { context?: ContextEntry[] }).context;
```

即使代码只有两行，这仍是重复的契约逻辑。每个消费者都拥有自己的《什么是有效载荷》的定义。
consumer now has its own definition of what a valid payload means.

**推荐**：将解码器、类型卫具或折射放在数据拥有者旁边：

```typescript
if (isThreadEvent(ev)) {
  renderThreadEvent(ev);
}
```

**规则**：若同一个无类型的载荷字段在 2+ 个位置被读取，在加入第三个读者之前先创建一个共享的类型卫具 / 归一化处理 / 折射。
shared type guard / normalizer / projection before adding a third reader.

---

## 何时抽取

**抽象场景**：
- 相同代码出现 3+ 次
- 逻辑复杂到可能出现 bug
- 多个人可能需要它

**不抽象场景**：
- 仅使用一次
- 一行就能解决
- 抽取会比重复更为复杂

---

## 批量修改之后

当你对多个文件做了类似修改：

1. **复查**：是否捕获了所有实例？
2. **搜索**：运行 grep 查找任何遗漏
3. **考虑**：是否应该抽取？

### Reducer 应该使用完备的结构

When state is derived from action-like values (`action`, `kind`, `status`,
`phase`), prefer a reducer with one `switch` over scattered `if/else` updates.

```typescript
// BAD - action-specific state transitions are hard to audit
if (action === "opened") { ... }
else if (action === "comment") { ... }
else if (action === "status") { ... }

// GOOD - one reducer owns the transition table
switch (event.action) {
  case "opened":
    ...
    return;
  case "comment":
    ...
    return;
}
```

这在事件日志是唯一准确源时重要。减函数是一个明确的重放模型；显示代码和命令都不应重复实现该重放模型。
documented replay model; display code and commands should not duplicate pieces
of that replay model.

---

## 提交前检查清单

- [ ] 已搜索现有的相似代码
- [ ] 没有应该共享却被复制粘贴的逻辑
- [ ] 没有在共享解码器之外重复提取未赋类型的载荷字段
- [ ] 常量在单一位置定义
- [ ] 相似的模式遵循相同的结构
- [ ] Reducer/action 转换集中在一个 reducer 或命令调度器中

---

## 陷阱：Python if/elif/else 完备检查

**Problem**: Python's if/elif/else chains have no compile-time exhaustive 检查。 When you add a new value to a `Literal` type (e.g., `Platform`), existing if/elif/else chains silently fall through to `else` with wrong defaults.

**现象**：新平台只部分生效—某些方法返回 Claude 的默认值而非平台专有值。不会报错。

**Example** (`cli_adapter.py`):
```python
# BAD: "gemini" falls through to else, returns "claude"
@property
def cli_name(self) -> str:
    if self.platform == "opencode":
        return "opencode"
    else:
        return "claude"  # gemini silently gets "claude"!

# GOOD: explicit branch for every platform
@property
def cli_name(self) -> str:
    if self.platform == "opencode":
        return "opencode"
    elif self.platform == "gemini":
        return "gemini"
    else:
        return "claude"
```

**预防**： When adding a new value to a Python `Literal` type, search for ALL if/elif/else chains that switch on that type and add explicit branches. Don't rely on `else` being correct for new values.

---

## 陷阱：产生相同输出的不对称机制

**Problem**: When two different mechanisms must produce the same file set (e.g., recursive directory copy for init vs. manual `files.set()` for update), structural changes (renaming, moving, adding subdirectories) only propagate through the automatic mechanism. The manual one silently drifts.

**现象**：初始化完美生效，但更新则在错误路径上创建文件或样本完全遗漏。

**Prevention**:
- **Best**: Eliminate the asymmetry — have the manual path call the automatic one (e.g., `collectTemplateFiles()` calls `getAllScripts()` instead of maintaining its own list)
- **若不对称不可避免**：添加一个比较两种机制输出的回归测试
- When migrating directory structures, search for ALL code paths that reference the old structure

**真实 example**: `trellis update` had a manual `files.set()` list for 11 scripts that `getAllScripts()` already tracked. Fix: replaced the manual list with a `for..of getAllScripts()` loop. See `update.ts` refactor in v0.4.0-beta.3.

---

## 模板文件注册（Trellis 专用）

When adding new files to `src/templates/trellis/scripts/`:

**Single registration point**: `src/templates/trellis/index.ts`

1. Add `export const xxxScript = readTemplate("scripts/path/file.py");`
2. Add to `getAllScripts()` Map

That's it. `commands/update.ts` uses `getAllScripts()` directly — no manual sync needed.

**为何 this matters**: Without registration in `getAllScripts()`, `trellis update` won't sync the file to user projects. Bug fixes and features won't propagate.

**History**: Before v0.4.0-beta.3, `update.ts` had its own hand-maintained file list that frequently fell out of sync with `getAllScripts()`. This caused 11 Python files to be silently skipped during `trellis update`. The fix was to eliminate the duplicate list and use `getAllScripts()` as the single source of truth.

### 新脚本快速检查清单

```bash
# After adding a new .py file, verify it's in getAllScripts():
grep -l "newFileName" src/templates/trellis/index.ts  # Should match
```

### 模板同步约定

`.trellis/scripts/` (dogfooded) and `packages/cli/src/templates/trellis/scripts/` (template) must stay identical. After editing `.trellis/scripts/`, always sync:

```bash
rsync -av --delete --exclude='__pycache__' .trellis/scripts/ packages/cli/src/templates/trellis/scripts/
```

**Gotcha**: Running rsync with wrong source/destination paths can create nested garbage directories (e.g., `.trellis/scripts/packages/cli/...`). Always double-check paths before running.
