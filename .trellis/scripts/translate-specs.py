#!/usr/bin/env python3
"""Translate .trellis/spec/**/*.md from English to Chinese.

Strategy:
1. Keep code blocks, paths, package names, identifiers, i18n keys, URLs unchanged
2. Translate ## headers, prose text, table headers
3. Use a comprehensive translation dictionary

Run:
    python3 .trellis/scripts/translate-specs.py
"""
import re
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_DIR = ROOT / '.trellis' / 'spec'

# Translation dictionary for common technical terms in markdown headers and prose.
# Multi-word phrases first for longest-match.
TRANSLATIONS = [
    ('## Best practices for', '## 最佳实践'),
    ('## Directory Structure', '## 目录结构'),
    ('## Component Guidelines', '## 组件指南'),
    ('## Custom Hooks', '## 自定义 Hooks'),
    ('## Custom Hooks Guidelines', '## 自定义 Hooks 指南'),
    ('## Hook Guidelines', '## Hook 指南'),
    ('## Hooks Guidelines', '## Hooks 指南'),
    ('## State Management', '## 状态管理'),
    ('## Quality Guidelines', '## 质量指南'),
    ('## Quality Check', '## 质量检查'),
    ('## Type Safety', '## 类型安全'),
    ('## Forbidden', '## 禁止'),
    ('## Conventions', '## 约定'),
    ('## Conventions for', '## 约定：'),
    ('## Rules', '## 规则'),
    ('## Overview', '## 概述'),
    ('## Notes', '## 说明'),
    ('## Tree', '## 目录树'),
    ('## Verified Tree', '## 验证过的目录树'),
    ('## Expected Tree', '## 预期目录树'),
    ('## Expected Conventions', '## 预期约定'),
    ('## Expected Config', '## 预期配置'),
    ('## Expected Naming', '## 预期命名'),
    ('## Expected Style', '## 预期代码风格'),
    ('## Expected Patterns', '## 预期模式'),
    ('## Expected Decision Tree', '## 预期决策树'),
    ('## Tree (verified', '## 目录树（已验证'),
    ('## Tree (template', '## 目录树（模板'),
    ('## Status', '## 状态'),
    ('## Goal', '## 目标'),
    ('## Version', '## 版本'),
    ('## Author', '## 作者'),
    ('## Tags', '## 标签'),
    ('## Project Structure', '## 项目结构'),
    ('## Available Built-ins', '## 可用的内置函数'),
    ('## Available built-ins', '## 可用的内置函数'),
    ('## Built-ins (always check first)', '## 内置函数（始终优先检查）'),
    ('## Built-ins (check these first)', '## 内置函数（首先检查这些）'),
    ('## Built-ins', '## 内置函数'),
    ('## Real Code Examples', '## 真实代码示例'),
    ('## Code Examples', '## 代码示例'),
    ('## Example', '## 示例'),
    ('## Examples', '## 示例'),
    ('## Usage', '## 用法'),
    ('## Usage from apps', '## 在应用中用法'),
    ('## Usage from', '## 从...引入'),
    ('## Pattern', '## 模式'),
    ('## Patterns', '## 模式'),
    ('## Pattern:', '## 模式：'),
    ('## Pattern (synthetic)', '## 模式（合成）'),
    ('## Required Patterns', '## 必需模式'),
    ('## Test', '## 测试'),
    ('## Tests', '## 测试'),
    ('## Tests (Recommended)', '## 测试（推荐）'),
    ('## Real Layout', '## 真实布局'),
    ('## Real Patterns', '## 真实模式'),
    ('## Real Type Usage', '## 真实类型用法'),
    ('## When to add a new token', '## 何时添加新 token'),
    ('## When to Use This Package', '## 何时使用本包'),
    ('## When to Use', '## 何时使用'),
    ('## When to', '## 何时'),
    ('## Add code examples', '## 添加代码示例'),
    ('## Forbidden Patterns', '## 禁止项'),
    ('## Forbidden Patterns (conventions, see Forbidden section in each file)', '## 禁止项（约定，请查看每个文件的禁止段）'),
    ('## Quality', '## 质量'),
    ('## Quality Check Command', '## 质量检查命令'),
    ('## Quality Gates', '## 质量门禁'),
    ('## Coding Style', '## 代码风格'),
    ('## Style', '## 代码风格'),
    ('## Naming', '## 命名约定'),
    ('## Naming Conventions', '## 命名约定'),
    ('## File Layout', '## 文件布局'),
    ('## Mock Server Components', '## Mock 服务端组件'),
    ('## Pinia Stores', '## Pinia 状态存储'),
    ('## Pinia Stores (canonical 3)', '## Pinia 状态存储（标准 3 个）'),
    ('## Cross-page State', '## 跨页面状态'),
    ('## Pre-Development Checklist', '## 开发前检查清单'),
    ('## How to Fill These Guidelines', '## 如何填写这些指南'),
    ('## How to Run', '## 如何运行'),
    ('## Hook', '## Hook'),
    ('## Hooks', '## Hooks'),
    ('## Persistence', '## 持久化'),
    ('## Why', '## 原因'),
    ('## Default', '## 默认'),
    ('## Goals', '## 目标'),
    ('## Background', '## 背景'),
    ('Default value for', '默认值：'),
    ('Default location', '默认位置'),
    ('Required for', '需要'),
    ('Do not', '不要'),
    ('When to use', '何时使用'),
    ('See also', '另见'),
    ('Per-package conventions', '每个包的约定'),
    ('At the package convention layer.', '用于包级约定层。'),
    ('At the frontend convention layer.', '用于前端约定层。'),
    ('At the convention layer for a specific package.', '用于某个具体包的约定层。'),
    ('Real patterns', '真实模式'),
    ('Real Vue typing patterns', '真实 Vue 类型模式'),
    ('Strict-mode TS via', '严格模式 TS 通过'),
    ('Strict-mode TS', '严格模式 TS'),
    ('Required Patterns', '必需模式'),
    ('Strict mode', '严格模式'),
    ('Type Imports', '类型导入'),
    ('Type Augmentation', '类型扩展'),
    ('Pre-commit Hooks', '提交前钩子'),
    ('Pre-commit hooks', '提交前钩子'),
    ('Pre-commit hooks (auto-fired)', '提交前钩子（自动触发）'),
    ('Lint / Format', 'Lint / Format'),
    ('Lint / Typecheck', 'Lint / 类型检查'),
    ('Lint / Typecheck Commands', 'Lint / 类型检查命令'),
    ('Lint / Type-check Commands', 'Lint / 类型检查命令'),
    ('Lint / Format commands:', 'Lint / Format 命令：'),
    ('Real quality rules (lint / format / typecheck / commit messages / forbidden patterns):', '真实质量规则（lint / format / typecheck / 提交信息 / 禁止项）：'),
    ('Headlines must be honest about what is documented', '标题必须与实际内容一致'),
    ('Guideline index for', '指南索引：'),
    ('Vue 3 +', 'Vue 3 + '),
    ('Vue 3 conventions', 'Vue 3 约定'),
    ('Vue 3 + UI-framework conventions.', 'Vue 3 + UI 框架约定。'),
    ('Vue 3 + UI-framework conventions', 'Vue 3 + UI 框架约定'),
    ('Vue 3 + UI-framework specific conventions for', 'Vue 3 + UI 框架（'),
    ('Vue 3 + Pinia conventions', 'Vue 3 + Pinia 约定'),
    ('Vue 3 conventions for', 'Vue 3 约定：'),
    ('Vue 3 component conventions', 'Vue 3 组件约定'),
    ('Vue 3 composables patterns', 'Vue 3 组合式函数模式'),
    ('Vue 3 state management patterns', 'Vue 3 状态管理模式'),
    ('TypeScript conventions (strict-mode TS / types / interfaces / type-only imports)', 'TypeScript 约定（严格模式 TS / 类型 / 接口 / type-only 导入）'),
    ('CSS / Tailwind conventions', 'CSS / Tailwind 约定'),
    ('When to use this package', '何时使用本包'),
    ('When the package is added', '当 package 添加时'),
    ('When the package is added:', '当 package 添加时：'),
    ('Replace these files with', '替换这些文件'),
    ('Replace these files with real content when the package is added.', '当 package 添加时，用真实内容替换这些文件。'),
    ('Replace these files with real content', '用真实内容替换这些文件'),
    ('Pure-function helpers', '纯函数 helpers'),
    ('Real layout', '真实布局'),
    ('Real Vue TypeScript patterns', '真实 Vue TypeScript 模式'),
    ('Pure data.', '纯数据。'),
    ('Pure data', '纯数据'),
    ('Pure functions only', '仅纯函数'),
    ('Real', '真实'),
    ('the package is added', 'package 添加后'),
    ('Strict-mode TS, zero runtime deps.', '严格模式 TS，无运行时依赖。'),
    ('Strict-mode TS.', '严格模式 TS。'),
    ('Zero-dep utilities', '零依赖 utilities'),
    ('Vue 3 + Pinia setup-style stores.', 'Vue 3 + Pinia setup 风格状态。'),
    ('Vue 3 + Pinia setup-style stores', 'Vue 3 + Pinia setup 风格状态'),
    ('No Vue hooks.', '无 Vue Hooks。'),
    ('No Vue Hooks', '无 Vue Hooks'),
    ('No Vue components.', '无 Vue 组件。'),
    ('No Vue Components', '无 Vue 组件'),
    ('Pure types package.', '纯类型包。'),
    ('Pure types package', '纯类型包'),
    ('NO Vue hooks here.', '这里无 Vue Hooks。'),
    ('NO Vue hooks here', '这里无 Vue Hooks'),
    ('Pure-function', '纯函数'),
    ('Pure constants / types package. No Vue hooks.', '纯常量 / 类型包。无 Vue Hooks。'),
    ('Here is a', '以下是'),
    ('Per-framework', '针对每个框架'),
    ('Per-Framework', '针对每个框架'),
    ('Per-ui-framework', '针对每个 UI 框架'),
    ('Per-UI-framework', '针对每个 UI 框架'),
    ('Do not use `any`.', '不要使用 `any`。'),
    ('Do not use `any`', '不要使用 `any`'),
    ('Do not enable strict mode per-file.', '不要在单文件上启用严格模式。'),
    ('Do not use `any` — use `unknown` and narrow.', '不要使用 `any`，请使用 `unknown` 并收窄类型。'),
    ('Do not depend on `cloneDeep` style utilities.', '不要依赖 `cloneDeep` 类风格的 utility。'),
    ('Do not introduce new utilities here.', '不要在此处引入新的 utility。'),
    ('Do not introduce new utility without bumping this package.', '未经升级 package，不要引入新 utility。'),
    ('Do not reimplement.', '不要重复实现。'),
    ('Do not reimplement what `@vben/foo / util` provide.', '不要重复实现 `@vben/foo/util` 已提供的功能。'),
    ('Do not implement against this phantom package.', '不要对幻影包实现具体代码。'),
    ('Do not implement against this phantom package before the real package exists.', '在该 phantom 包真实存在前不要实现。'),
    ('Do not implement against this placeholder before the real package exists.', '在该 phantom 包真实存在前不要实现。'),
    ('Do not add Vue code.', '不要添加 Vue 代码。'),
    ('Do not add Vue refs.', '不要添加 Vue ref。'),
    ('Do not add Vue-specific code.', '不要添加 Vue 专属代码。'),
    ('Do not add real auth here.', '不要在这里加真实鉴权。'),
    ('Do not add real auth here - mock only.', '不要在此添加真实鉴权 - 仅 mock。'),
    ('Do not add a real database.', '不要添加真实数据库。'),
    ('Do not add IO (network, fs) — only pure helpers.', '不要添加 IO（网络、文件系统）— 仅纯 helpers。'),
    ('Unless absolutely necessary.', '除非绝对必要。'),
    ('Unless absolutely necessary', '除非绝对必要'),
    ('Unless required by doc-style extension.', '除非文档类型扩展需要。'),
    ('See also [Type Safety](./type-safety.md).', '另见[类型安全](./type-safety.md)。'),
    ('See [type-safety.md](./type-safety.md)', '见 [type-safety.md](./type-safety.md)'),
    ('See [quality-guidelines.md](./quality-guidelines.md)', '见 [quality-guidelines.md](./quality-guidelines.md)'),
    ('See [hook-guidelines.md](./hook-guidelines.md)', '见 [hook-guidelines.md](./hook-guidelines.md)'),
    ('See [state-management.md](./state-management.md)', '见 [state-management.md](./state-management.md)'),
    ('Best practices for', '最佳实践：'),
    ('How frontend code is organized', '前端代码如何组织'),
    ('in this project.', '在本项目中。'),
    ('in this project', '在本项目中'),
    ('Detailed guidelines for', '本'),
    ('detailed guidelines.', '详细指南。'),
    ('Detailed guidelines.', '详细指南。'),
    ('instructions.', '说明。'),
    ('instructions', '说明'),
    ('Replace this with project conventions.', '替换为本项目约定。'),
    ('Replace this with project-specific conventions.', '替换为本项目约定。'),
    ('Document your', '写出'),
    ('## Mock Server', '## Mock 服务端'),
    ('## State', '## 状态'),
    ('## Types', '## 类型'),
    ('## Required tools', '## 必需工具'),
    ('## Plugin', '## 插件'),
    ('## Testing', '## 测试'),
    ('## Test Conventions', '## 测试约定'),
    ('## Test setup', '## 测试设置'),
    ('## Generated Files', '## 生成的文件'),
    ('## Config', '## 配置'),
    ('## Architecture', '## 架构'),
    ('## Workflow', '## 工作流'),
    ('## Description', '## 描述'),
    ('## Frontend', '## 前端'),
    ('## Backend', '## 后端'),
    ('## Component', '## 组件'),
    ('## Components', '## 组件'),
    ('## Service', '## 服务'),
    ('## Layouts', '## 布局'),
    ('## Lints', '## Lint 规则'),
    ('## Lint', '## Lint'),
    ('## Layout UI primitives', '## 布局 UI 原子组件'),
    ('A real layout for', '真实布局：'),
    ('A real Vue 3 + Ant Design Vue layout for', 'Vue 3 + Ant Design Vue 真实布局：'),
    ('A real Vue 3 + Element Plus layout for', 'Vue 3 + Element Plus 真实布局：'),
    ('A real Vue 3 + Naive UI layout for', 'Vue 3 + Naive UI 真实布局：'),
    ('Vue 3 + TDesign Vue Next conventions for', 'Vue 3 + TDesign Vue Next 约定：'),
    ('Vue 3 + VbenForm conventions for', 'Vue 3 + VbenForm 约定：'),
    ('Vue 3 conventions used across', 'Vue 3 约定，用于'),
    ('Vue 3 + TypeScript strict mode conventions for', 'Vue 3 + TypeScript 严格模式约定：'),
    ('Vue 3 + TypeScript component patterns for', 'Vue 3 + TypeScript 组件模式：'),
    ('Vue 3 + icon-set conventions for', 'Vue 3 + 图标约定：'),
    ('TypeScript strict-mode TS plus Vue 3 conventions for', 'TypeScript 严格模式 TS 加 Vue 3 约定：'),
    ('Vue 3 + CSS for', 'Vue 3 + CSS：'),
    ('Vue 3 + Helper Lib conventions for', 'Vue 3 + Helper 库约定：'),
    ('Vue 3 + Hook conventions for', 'Vue 3 + Hook 约定：'),
    ('Vue 3 + Composables patterns for', 'Vue 3 + 组合式函数模式：'),
    ('Vue 3 + Component patterns for', 'Vue 3 + 组件模式：'),
    ('Vue 3 + Quality guidelines for', 'Vue 3 + 质量指南：'),
    ('Vue 3 + Router patterns for', 'Vue 3 + 路由模式：'),
    ('Vue 3 + Nitro mock server conventions for', 'Vue 3 + Nitro mock 服务端约定：'),
    ('Vue 3 + Pinia conventions for', 'Vue 3 + Pinia 约定：'),
    ('Vue 3 + State management patterns for', 'Vue 3 + 状态管理模式：'),
    ('Vue 3 + TipTap (rich text editor) conventions for', 'Vue 3 + TipTap（富文本编辑器）约定：'),
    ('A Vue 3 conventions', 'Vue 3 约定'),
    ('A hooks guidelines', 'Hooks 指南'),
    ('A Vue 3', 'Vue 3'),
    ('(this project)', '（本项目）'),
    ('TypeScript strict mode is required.', 'TypeScript 严格模式是必需的。'),
    ('TypeScript strict mode is required', 'TypeScript 严格模式是必需的'),
    ('TypeScript strict mode', 'TypeScript 严格模式'),
    ('A Vue 3 Conventions', 'Vue 3 约定'),
    ('Vue 3 Type Safety', 'Vue 3 类型安全'),
    ('Vue 3 Quality', 'Vue 3 质量'),
    ('Vue 3 Hooks', 'Vue 3 Hooks'),
    ('Vue 3 State Management', 'Vue 3 状态管理'),
    ('Vue 3 Components', 'Vue 3 组件'),
    ('Vue 3 State', 'Vue 3 状态'),
    ('Vue 3 Convention', 'Vue 3 约定'),
    ('Layouts Conventions', '布局约定'),
    ('Layouts Conventions.', '布局约定。'),
    ('Strict-mode TypeScript', '严格模式 TypeScript'),
    ('Strict-mode TypeScript.', '严格模式 TypeScript。'),
    ('Pinia Stores', 'Pinia 状态'),
    ('Pinia store', 'Pinia store'),
    ('TS Conventions', 'TS 约定'),
    ('Lint Conventions', 'Lint 约定'),
    ('Hook Conventions', 'Hook 约定'),
    ('Type Conventions', '类型约定'),
    ('Quality Conventions', '质量约定'),
    ('Vue 3 + ', 'Vue 3 + '),
    ('Vue 3 ', 'Vue 3 '),
    ('in frontend.', '在前端层。'),
    ('in backend.', '在后端层。'),
    ('Vue 3 + TDesign', 'Vue 3 + TDesign'),
    ('Vue 3 + VbenForm', 'Vue 3 + VbenForm'),
    ('Conventions.', '约定。'),
    ('Conventions', '约定'),
    ('Vue 3 Conventions', 'Vue 3 约定'),
    ('Vue 3 Conventions.', 'Vue 3 约定。'),
    ('Vue 3 + TS Conventions', 'Vue 3 + TS 约定'),
    ('Vue 3 + TS Conventions.', 'Vue 3 + TS 约定。'),
    ('Vue 3 + Utility conventions for', 'Vue 3 + Utility 约定：'),
    ('Vue 3 + Persisted Pinia conventions for', 'Vue 3 + 持久化 Pinia 约定：'),
    ('Vue 3 + Tailwind conventions for', 'Vue 3 + Tailwind 约定：'),
    ('Vue 3 + Helper', 'Vue 3 + Helper'),
    ('Vue 3 + Composable', 'Vue 3 + Composable'),
    ('Vue 3 + Pinia', 'Vue 3 + Pinia'),
    ('Vue 3 + i18n', 'Vue 3 + i18n'),
    ('Vue 3 + Vue', 'Vue 3 + Vue'),
    ('Vue 3 + Nitro', 'Vue 3 + Nitro'),
    ('Vue 3 + Quality', 'Vue 3 + 质量'),
    ('Vue 3 + Type Safety', 'Vue 3 + 类型安全'),
    ('Vue 3 + Form', 'Vue 3 + 表单'),
    ('Vue 3 + Composables', 'Vue 3 + 组合式函数'),
]


def is_code_line(line: str) -> bool:
    """Detect whether the line is part of a code block."""
    return line.startswith('```') or line.startswith('|') or '`@' in line or '@vben' in line and '`' in line


def is_in_code_block(lines, idx):
    """Check if line idx is inside a code block."""
    in_block = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_block = not in_block
        if i == idx:
            return in_block
    return False


def translate_line(line: str) -> str:
    """Translate a markdown line - apply translations but preserve code."""
    # Skip pure code lines
    stripped = line.strip()
    if stripped.startswith('```'):
        return line
    # Skip code inside ``` blocks? Already handled by is_in_code_block.
    return line


def translate_file_text(text: str) -> str:
    """Apply translations to a markdown file body."""
    lines = text.split('\n')
    out = []
    in_code = False
    for line in lines:
        # Track code block state
        if line.strip().startswith('```'):
            in_code = not in_code
            out.append(line)
            continue

        if in_code:
            out.append(line)
            continue

        # Translate headers + prose lines
        translated = line
        for en, zh in TRANSLATIONS:
            if en in translated:
                translated = translated.replace(en, zh)
        out.append(translated)
    return '\n'.join(out)


def main():
    files_changed = 0
    files_total = 0

    for md_file in sorted(SPEC_DIR.rglob('*.md')):
        files_total += 1
        try:
            text = md_file.read_text()
        except Exception:
            continue

        new_text = translate_file_text(text)
        if new_text != text:
            md_file.write_text(new_text)
            files_changed += 1

    print(f'Processed {files_total} files, translated {files_changed}')


if __name__ == '__main__':
    main()
