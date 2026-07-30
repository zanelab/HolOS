# 思考指南

> **Purpose**: Expand your thinking to catch things you might not have considered.

---

## 为什么需要思考指南？

**Most bugs and tech debt come from "didn't think of that"**, not from lack of skill:

- 未考虑层边界会发生什么 → 跨层 bug
- 未考虑代码模式重复 → 代码全面重复
- 未考虑极端情况 → 运行时错误
- 未考虑未来维护人员 → 代码难以阅读

These guides help you **ask the right questions before coding**.

---

## 可用的指南

| Guide | Purpose | When to Use |
|-------|---------|-------------|
| [Code Reuse Thinking Guide](./code-reuse-thinking-guide.md) | Identify patterns and reduce duplication | When you notice repeated patterns |
| [Cross-Layer Thinking Guide](./cross-layer-thinking-guide.md) | Think through data flow across layers | Features spanning multiple layers |

---

## 快速参考：思考触发点

### 何时考虑跨层问题

- [ ] Feature touches 3+ layers (API, Service, Component, Database)
- [ ] 层与层之间数据格式发生变化
- [ ] 多个消费者需要同样的数据
- [ ] 你不确定某些逻辑该放在哪里
- [ ] You are adding an event kind, JSONL record, RPC payload, or config field
- [ ] UI / command code starts casting raw payload fields directly

→ Read [Cross-Layer Thinking Guide](./cross-layer-thinking-guide.md)

### 何时考虑代码复用

- [ ] 你正在编写与已有代码相似的代码
- [ ] 你看到同一模式重复了 3 次以上
- [ ] 你正在多个位置添加新字段
- [ ] **你正在修改任何常量或配置**
- [ ] **你正在创建新的工具/辅助函数** ← 先搜索！
- [ ] 两个文件使用局部强转读取同一个无类型的载荷字段
- [ ] Multiple branches update the same derived state from `kind` / `action`

→ Read [Code Reuse Thinking Guide](./code-reuse-thinking-guide.md)

### When Verifying AI Cross-Review Results

- [ ] Reviewer claims "user input can be malicious" → Check the actual data source (internal manifest? user config? external API?)
- [ ] 审议者标注"缺失校验" → 数据是否来自可信的内部源？
- [ ] 审议者称"行为变化" → 阅读代码注释 — 是否为敏质设计？
- [ ] 审议者标出测试中的 "bug" → 心里删除正在测试的功能 — 测试仍然通过吗？如是→ 同谓复辝测试

**Common AI reviewer false-positive patterns**:
1. **Trust boundary confusion**: Treating internal data (bundled JSON manifests) as untrusted external input
2. **忽略设计注释**：将代码注释中说明的敏质行为作为 bug 提出
3. **Variable misreading**: Not tracing a variable to its actual definition (e.g., Map keyed by path vs name)

**Verification rule**: Every CRITICAL/WARNING finding 必须是 verified against the actual code before prioritizing. Budget ~35% false-positive rate for AI reviews.

---

## Pre-Modification Rule (CRITICAL)

> **Before changing ANY value, ALWAYS search first!**

```bash
# Search for the value you're about to change
grep -r "value_to_change" .
```

This single habit prevents most "forgot to update X" bugs.

---

## 如何使用本目录

1. **写代码之前**：浏览相关思考指南
2. **写代码期间**：若感觉某处重复或复杂，查阅指南
3. **Bug 之后**：将新的启发补充到指南中（从错误中学习）

---

## 贡献

Found a new "didn't think of that" moment? Add it to the relevant guide.

---

**Core Principle**: 30 minutes of thinking saves 3 hours of debugging.
