
# Deep translate remaining English prose to Chinese via sub-agents

## Goal

之前 3-pass 翻译:
- Pass 1: 576/580 files (rules-based header phrases)
- Pass 2: 161 files (Vue 3 + X patterns)
- Pass 3: 65 files (more Vue 3 + X patterns)

但 ~20% 的 contextual prose 句子 仍英文。

本次 task: 用 **delegate_task** (parallel sub-agents) 在 background 真正翻译剩余英文 prose 句子。

## Strategy

1. Phase 2.1 — Implementation:
   - 找 spec files 还有英文 prose (≥ 50% 英文 still)
   - Divide into 3 batches (~150-200 files each)
   - delegate_task (parallel, max 3 concurrent) for each batch
   - 每个 sub-agent 翻译 ≥ 100 .md 文件,preserve code blocks, paths, identifiers

2. Phase 3.4 — commit per batch

## Acceptance Criteria

- [ ] 剩余 ≥ 50% English prose 翻译成 Chinese
- [ ] Code blocks / paths / identifiers / i18n keys preserved
- [ ] Commits: per sub-agent batch
- [ ] No defensive verbatim changes
- [ ] Cleanup + archive

## Notes

- 期望 3 sub-agent batches
- 每个 agent 处理 ~150 .md files (~30 分钟)
- 3 batches parallel = ~30-45 min total wall clock
