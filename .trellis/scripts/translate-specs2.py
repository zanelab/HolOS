#!/usr/bin/env python3
"""Phase 2 translation: convert remaining English prose sentences to Chinese.

Strategy: Use line-by-line detection of "prose-only" English sentences and
translate common patterns. Run after translate-specs.py.

Run:
    python3 .trellis/scripts/translate-specs2.py
"""
import re
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_DIR = ROOT / '.trellis' / 'spec'

# Second-pass translations: targeted at common prose sentences.
TRANSLATIONS = [
    # ===== Sentence-style prose (only match in non-code lines) =====
    ('A UI-framework component adapter.', 'UI 框架组件适配器。'),
    ('A UI-framework component adapter', 'UI 框架组件适配器'),
    ('Package is consumed via workspace alias.', '本包通过 workspace 别名消费。'),
    ('Package is consumed via', '本包通过...消费'),
    ('Re-export via `src/index.ts` — single entry, no internal deep imports.', '通过 `src/index.ts` re-export —— 单一入口，不做内部深导入。'),
    ('Re-export via `src/index.ts` — single entry, no internal deep imports', '通过 `src/index.ts` re-export —— 单一入口，不做内部深导入'),
    ('Use `\'.\'` relative imports for sibling files; use workspace name for cross-package imports.', '同级文件使用 `\'.\'` 相对路径导入；跨包导入使用 workspace 名称。'),
    ('Use `\'.\'` relative imports', '同级文件使用 `\'.\'` 相对路径导入'),
    ('Test on at least 1 app', '至少在 1 个应用中测试'),
    ('Type-bump is mandatory when adding new rules.', '添加新规则时必须升级 package 版本。'),
    ('Version bump is mandatory when adding new rules to', '在...中添加新规则时必须升级版本'),
    ('Version bump is mandatory', '必须升级版本'),
    ('Adopted from the team\'s + ESLint flat config + OxFmt + Stylelint.', '采用自团队 + ESLint flat config + OxFmt + Stylelint。'),

    # App-level
    ('Vite + Vue 3 + TS, port 5666-ish', 'Vite + Vue 3 + TS，端口约 5666'),
    ('(configured in `vite.config.ts`).', '（在 `vite.config.ts` 中配置）。'),
    ('Use `defineOverridesPreferences` from `src/preferences.ts` to override defaults.', '使用 `src/preferences.ts` 的 `defineOverridesPreferences` 覆盖默认值。'),
    ('i18n keys live in', 'i18n keys 放在'),
    ('Routes:', '路由：'),
    ('`core.ts` (BasicLayout/Auth/404)', '`core.ts`（BasicLayout / Auth / 404）'),
    ('Custom layouts override', '自定义布局覆盖'),

    # Lib
    ('Single `src/index.ts` entry — re-export public API only', '单一 `src/index.ts` 入口 —— 只 re-export 公开 API'),
    ('Internal helpers stay in `helpers/` or `utils/` subdirs', '内部 helpers 放在 `helpers/` 或 `utils/` 子目录'),
    ('Use TypeScript strict mode; no `any` (use `unknown` + narrowing)', '使用 TypeScript 严格模式；禁止 `any`（用 `unknown` 并收窄类型）'),
    ('Use TS strict mode', '使用 TS 严格模式'),
    ('Use `from "@vben` workspace alias', '使用 `@vben/...` workspace 别名'),

    # Layout
    ('Layout components export named functions returning `import(...).then(m => m.X)`', '布局组件导出 named 函数，返回 `import(...).then(m => m.X)`'),
    ('Use `@vben-core/layout-ui` primitives', '使用 `@vben-core/layout-ui` 原子组件'),
    ('Sidebar / Tabbar / Header widths/visibility driven by `preferences` store', '侧栏 / Tabbar / Header 的宽度与可见性由 `preferences` store 驱动'),

    # Hooks
    ('Don\'t write new hooks unless absolutely necessary', '除非绝对必要，否则不要写新 hooks'),
    ('Not allowed by Vben v5.7.0 conventions.', '违反 vben v5.7.0 约定。'),

    # Auth
    ('Tree-shaking is critical', 'Tree-shaking 关键'),

    # Status & accessibility
    ('Status code', '状态码'),
    ('Return type', '返回类型'),
    ('Real usage', '真实用法'),
    ('Real layouts', '真实布局'),
    ('Real Vue TypeScript strict-mode TS', '真实 Vue TypeScript 严格模式 TS'),

    # Header specifics
    ('Component Naming', '组件命名'),
    ('Props', 'Props'),
    ('Props.', 'Props。'),
    ('Emits', 'Emits'),
    ('Slots', 'Slots'),
    ('v-model', 'v-model'),

    # Misc
    ('Frontend, Backend.', '前端、后端。'),
    ('Frontend, Backend', '前端、后端'),
    ('Tagged for:', '标签：'),
    ('Tags:', '标签：'),
    ('Tag Taxonomy', '标签分类'),
    ('Total pages', '总页数'),
    ('Total pages.', '总页数。'),
    ('Page Thresholds', '页面阈值'),

    # More prose
    ('a Vue 3', 'Vue 3'),
    ('Vue 3', 'Vue 3'),
    ('Strict mode', '严格模式'),
    ('Vue 3 conventions', 'Vue 3 约定'),

    # Common phrases in README
    ('This project is', '本项目'),
    ('This package is', '本包'),
    ('This directory contains', '本目录包含'),
    ('This package provides', '本包提供'),
    ('This package contains', '本包包含'),
    ('The reasoning and tradeoffs', '理由与权衡'),
    ('A typical task looks like', '典型任务'),

    # 测试相关
    ('Real test', '真实测试'),
    ('Real Vue 3 + Pinia test', '真实 Vue 3 + Pinia 测试'),
    ('Real Vue 3 + TypeScript strict-mode TS test', '真实 Vue 3 + TypeScript 严格模式 TS 测试'),
    ('Real Vue 3 + Helper Lib test', '真实 Vue 3 + Helper 库测试'),
    ('Real Vue 3 + Toast test', '真实 Vue 3 + Toast 测试'),

    # 'Plain English' levels
    ('Real Vue 3', '真实 Vue 3'),
    ('Plain English', '自然英文'),
    ('Plain Chinese', '简体中文'),

    # "required / recommended"
    ('Required for', '需要'),
    ('Recommended for', '推荐给'),
    ('Optional for', '可选给'),

    # Common
    ('hooks below.', 'hooks 如下。'),
    ('hooks below', 'hooks 如下'),
    ('composition below.', '组合式函数如下。'),
    ('composition below', '组合式函数如下'),
    ('state management below.', '状态管理如下。'),
    ('state management below', '状态管理如下'),
    ('test below.', '测试如下。'),
    ('test below', '测试如下'),
    ('below.', '如下。'),
    ('below:', '如下：'),
    ('What not to do.', '不要做什么。'),
    ('What not to do', '不要做什么'),
    ('What to do.', '应该做什么。'),
    ('What to do', '应该做什么'),
    ('When to fill', '何时填写'),
    ('How to use', '如何使用'),

    # Real-world style
    ('Real Vue 3 + Helper conventions.', '真实 Vue 3 + Helper 约定。'),
    ('Real Vue 3 + Helper Lib conventions for', '真实 Vue 3 + Helper Lib 约定：'),

    # 'This package'
    ('This package', '本包'),
    ('this package', '本包'),

    # 'Please refer to'
    ('Please refer to', '请参见'),
    ('Refer to', '参见'),

    # Misc
    ('Available at', '可用在'),
    ('See types.ts for full enum', '见 types.ts 完整 enum'),
    ('See lib docs for', '见 lib 文档'),
    ('See component docs for', '见组件文档'),
    ('specific patterns below.', '特定模式如下。'),
    ('specific patterns below', '特定模式如下'),
    ('note that', '请注意'),
    ('Note that', '请注意'),

    # Real-world
    ('Real Composition', '真实组合'),
    ('Real Composition API conventions', '真实 Composition API 约定'),

    # Misc
    ('Vue 3 conventions for', 'Vue 3 约定：'),
    ('Vue 3 + Helper', 'Vue 3 + Helper'),
    ('Vue 3 + Pinia', 'Vue 3 + Pinia'),
    ('Vue 3 + Type', 'Vue 3 + Type'),
    ('Vue 3 + Toast', 'Vue 3 + Toast'),
    ('Vue 3 + Tree', 'Vue 3 + Tree'),
    ('Vue 3 + Virtual', 'Vue 3 + Virtual'),
    ('Vue 3 + Theme', 'Vue 3 + 主题'),
    ('Vue 3 + Vben', 'Vue 3 + Vben'),
    ('Vue 3 + Constants', 'Vue 3 + Constants'),
    ('Vue 3 + State', 'Vue 3 + 状态'),
    ('Vue 3 + Router', 'Vue 3 + 路由'),
    ('Vue 3 + Hook', 'Vue 3 + Hook'),
    ('Vue 3 + Form', 'Vue 3 + 表单'),
    ('Vue 3 + VxeTable', 'Vue 3 + VxeTable'),
    ('Vue 3 + TipTap', 'Vue 3 + TipTap'),

    # final cleanup
    ('Vue 3 Conventions', 'Vue 3 约定'),
    ('Vue 3 Conventions.', 'Vue 3 约定。'),
    ('Vue 3 + Tab', 'Vue 3 + Tab'),
    ('Vue 3 + Captcha', 'Vue 3 + 验证码'),
    ('Vue 3 + Pinia conventions.', 'Vue 3 + Pinia 约定。'),
    ('Vue 3 + Pinia conventions', 'Vue 3 + Pinia 约定'),
    ('Vue 3 + Helper Lib', 'Vue 3 + Helper 库'),
    ('Vue 3 + Helper Lib conventions', 'Vue 3 + Helper 库约定'),
    ('Vue 3 + Helper Lib conventions.', 'Vue 3 + Helper 库约定。'),
    ('Vue 3 + TS', 'Vue 3 + TS'),
    ('Vue 3 + TDesign', 'Vue 3 + TDesign'),
    ('Vue 3 + Ant', 'Vue 3 + Ant'),
    ('Vue 3 + Element', 'Vue 3 + Element'),
    ('Vue 3 + Naive', 'Vue 3 + Naive'),
    ('Vue 3 + Style', 'Vue 3 + 样式'),

    # Real + Vue 3
    ('Real Vue 3 conventions.', '真实 Vue 3 约定。'),
    ('Real Vue 3 conventions', '真实 Vue 3 约定'),

    # Final tail
    ('Vue 3 Conventions.', 'Vue 3 约定。'),

    # Raw prose
    ('Vue 3 + Tailwind', 'Vue 3 + Tailwind'),
    ('Vue 3 + Tab', 'Vue 3 + Tab'),
    ('Vue 3 + VbenForm', 'Vue 3 + VbenForm'),
    ('Vue 3 + Request', 'Vue 3 + Request'),
    ('Vue 3 + Popup', 'Vue 3 + Popup'),
    ('Vue 3 + Menu', 'Vue 3 + 菜单'),
    ('Vue 3 + Layout', 'Vue 3 + 布局'),
    ('Vue 3 + Icon', 'Vue 3 + 图标'),
    ('Vue 3 + Hook', 'Vue 3 + Hook'),
    ('Vue 3 + Form', 'Vue 3 + 表单'),
    ('Vue 3 + Util', 'Vue 3 + Util'),
    ('Vue 3 + Helper', 'Vue 3 + Helper'),
    ('Vue 3 + Type', 'Vue 3 + 类型'),
    ('Vue 3 + Utility', 'Vue 3 + Utility'),
    ('Vue 3 + UI', 'Vue 3 + UI'),
    ('Vue 3 + State', 'Vue 3 + 状态'),
    ('Vue 3 + Quality', 'Vue 3 + 质量'),
    ('Vue 3 + Hooks', 'Vue 3 + Hooks'),
    ('Vue 3 + Component', 'Vue 3 + 组件'),
    ('Vue 3 + Components', 'Vue 3 + 组件'),
    ('Vue 3 + Conventions', 'Vue 3 + 约定'),
    ('Vue 3 + Custom', 'Vue 3 + 自定义'),
    ('Vue 3 + Custom Hook', 'Vue 3 + 自定义 Hook'),
    ('Vue 3 + Custom Hooks', 'Vue 3 + 自定义 Hooks'),
    ('Vue 3 + Effect', 'Vue 3 + Effect'),

    # Real + spec
    ('Real Vue 3 + Pinia setup-style store.', '真实 Vue 3 + Pinia setup 风格 store。'),
    ('Real Vue 3 + Nitro mock-server.', '真实 Vue 3 + Nitro mock 服务端。'),
    ('Real Vue 3 + Nitro mock server', '真实 Vue 3 + Nitro mock 服务端'),
    ('Real Vue 3 + Persisted store.', '真实 Vue 3 + 持久化 store。'),
    ('Real Vue 3 + Persisted Pinia store.', '真实 Vue 3 + 持久化 Pinia store。'),
    ('Real Vue 3 + Persisted Pinia', '真实 Vue 3 + 持久化 Pinia'),

    # CR-LF safe
    ('Vue 3 + Composables', 'Vue 3 + 组合式函数'),
    ('Vue 3 + Layout UI', 'Vue 3 + 布局 UI'),
    ('Vue 3 + Common', 'Vue 3 + 通用'),
    ('Vue 3 + Toolkit', 'Vue 3 + 工具包'),

    # Real + name
    ('Real Vue 3 + request', '真实 Vue 3 + request'),
    ('Real Vue 3 + style', '真实 Vue 3 + 样式'),
    ('Real Vue 3 + i18n', '真实 Vue 3 + i18n'),
    ('Real Vue 3 + utils', '真实 Vue 3 + 工具'),
    ('Real Vue 3 + types', '真实 Vue 3 + 类型'),
    ('Real Vue 3 + options', '真实 Vue 3 + 选项'),

    # Generic English fragments
    ('Real ', '真实 '),
    ('real-world', '真实'),
    ('Real-world', '真实'),

    # Type-safety
    ('Strict-mode TS', '严格模式 TS'),
]


def is_in_code(lines, idx):
    in_code = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code = not in_code
        if i == idx:
            return in_code
    return False


def translate_file(text):
    lines = text.split('\n')
    out = []
    for idx, line in enumerate(lines):
        if is_in_code(lines, idx):
            out.append(line)
            continue
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
        new_text = translate_file(text)
        if new_text != text:
            md_file.write_text(new_text)
            files_changed += 1
    print(f'Processed {files_total} files, translated {files_changed}')


if __name__ == '__main__':
    main()