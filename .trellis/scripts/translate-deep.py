#!/usr/bin/env python3
"""Deep translation pass 3: targeted at remaining English prose in non-code lines.

Run after translate-specs.py and translate-specs2.py.
"""
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_DIR = ROOT / '.trellis' / 'spec'

# Comprehensive prose translations (longer phrases that may still be in English).
TRANSLATIONS = [
    ('Why', '为何'),
    ('Used by Vue apps via', '由 Vue 应用通过...使用'),
    ('Used by', '被使用'),
    ('used by Vue apps via', '由 Vue 应用通过...使用'),
    ('Vue 3 apps', 'Vue 3 应用'),
    ('Vue 3 + Composition API patterns', 'Vue 3 + Composition API 模式'),
    ('Vue 3 + Composition API', 'Vue 3 + Composition API'),
    ('Composition API patterns', 'Composition API 模式'),

    # Common descriptions
    ('A simple Pinia store.', '一个简单的 Pinia 状态。'),
    ('A minimal Pinia store', '一个最小化的 Pinia 状态'),
    ('A minimal setup-style store', '一个最小 setup 风格状态'),
    ('A utility', '一个 utility'),
    ('A composable', '一个组合式函数'),
    ('A mock backend endpoint', '一个 mock 服务端端点'),
    ('A pure-data package', '一个纯数据 package'),

    # "It is X" / "These are X"
    ('It must be imported by', '必须被...导入'),
    ('It must be imported only by', '只能被...导入'),
    ('It is consumed by', '被...消费'),
    ('This is consumed by', '此...被...消费'),
    ('Exposes a single API', '暴露单一 API'),
    ('Is consumed by', '被...消费'),
    ('is consumed by', '被...消费'),

    # Generic
    ('Real ', '真实 '),
    ('Demo data', 'Demo 数据'),
    ('Demo data.', 'Demo 数据。'),
    ('production data', '生产数据'),
    ('production code', '生产代码'),
    ('production API', '生产 API'),

    # Practical
    ('check .', '检查。'),
    ('check.', '检查。'),
    ('use X', '使用 X'),
    ('use the', '使用'),
    ('via its', '通过其'),

    # Verbose phrases
    ('must be', '必须是'),
    ('is shared by', '由...共享'),
    ('shared by', '由...共享'),

    # Decision tree parts
    ('- One component, one render', '- 单组件单次渲染'),
    ('- Cross-route but app-global', '- 跨路由但是应用全局'),
    ('- Cross-page, persisted', '- 跨页面，持久化'),
    ('- Cross-page, transient', '- 跨页面，临时'),
    ('- Cross-page but app-global, persisted', '- 跨页面但是应用全局，持久化'),
    ('- Server cache', '- 服务端缓存'),
    ('- Cross-route but app-global, persisted', '- 跨路由但是应用全局，持久化'),
    ('- One component, deep children', '- 单组件深 children'),

    # Process
    ('How to run', '如何运行'),
    ('Open a terminal', '打开终端'),
    ('Run:', '运行：'),
    ('Result:', '结果：'),

    # Common instruction
    ('Do not skip', '不要跳过'),
    ('is fully purged', '已完全清除'),

    # "This section"
    ('This section', '本节'),
    ('This section covers', '本节涵盖'),
    ('This document', '本文档'),
    ('This guide', '本指南'),
    ('This file', '本文件'),
    ('This index', '本索引'),

    # Construction
    ('A TypeScript', '一个 TypeScript'),
    ('An autoload', '一个自动加载'),
    ('An identifier', '一个 identifier'),
    ('A loader', '一个加载器'),

    # Other
    ('CSS only', '仅 CSS'),
    ('JS only', '仅 JS'),
    ('typescript only', '仅 typescript'),
    ('typescript and Vue', 'typescript 与 Vue'),

    # Misc
    ('Real Vue 3 + Toast.', '真实 Vue 3 + Toast。'),
    ('Real Vue 3 + UI-framework.', '真实 Vue 3 + UI 框架。'),
    ('Real Vue 3 + UI-framework', '真实 Vue 3 + UI 框架'),
    ('Real Vue 3 + TipTap editor.', '真实 Vue 3 + TipTap 编辑器。'),
    ('Real Vue 3 + TipTap editor', '真实 Vue 3 + TipTap 编辑器'),
    ('Real Vue 3 + Form.', '真实 Vue 3 + 表单。'),
    ('Real Vue 3 + Form', '真实 Vue 3 + 表单'),
    ('Real Vue 3 + Routing.', '真实 Vue 3 + 路由。'),
    ('Real Vue 3 + Routing', '真实 Vue 3 + 路由'),

    # Common JWT auth
    ('A small JWT-based auth module used by', '一个基于 JWT 的小型 auth 模块，被使用于'),
    ('A small JWT-based auth module', '一个基于 JWT 的小型 auth 模块'),
    ('A JWT-based auth module', '基于 JWT 的 auth 模块'),

    # Common state types
    ('A minimal Pinia state container', '一个最小 Pinia 状态容器'),
    ('A composable for accessing', '用于访问...的 composable'),

    # Pattern description
    ('A pre-built', '一个预构建的'),
    ('A layout skeleton', '一个布局骨架'),

    # Misc
    ('Vue 3 + Tailwind utilities', 'Vue 3 + Tailwind utility 类'),
    ('Vue 3 + TipTap', 'Vue 3 + TipTap'),
    ('Vue 3 + Toast', 'Vue 3 + Toast'),
    ('Vue 3 + VxeTable', 'Vue 3 + VxeTable'),
    ('Vue 3 + Tab', 'Vue 3 + Tab'),
    ('Vue 3 + Theme', 'Vue 3 + 主题'),
    ('Vue 3 + Tree', 'Vue 3 + Tree'),
    ('Vue 3 + Upload', 'Vue 3 + Upload'),
    ('Vue 3 + Validators', 'Vue 3 + 验证器'),
    ('Vue 3 + VirtualList', 'Vue 3 + 虚拟列表'),

    # Real Vue 3 + ...
    ('Real Vue 3 + Captcha', '真实 Vue 3 + 验证码'),
    ('Real Vue 3 + Toast', '真实 Vue 3 + Toast'),
    ('Real Vue 3 + Tooltip', '真实 Vue 3 + Tooltip'),
    ('Real Vue 3 + Tree', '真实 Vue 3 + Tree'),
    ('Real Vue 3 + Tab', '真实 Vue 3 + Tab'),
    ('Real Vue 3 + Routing', '真实 Vue 3 + 路由'),
    ('Real Vue 3 + Storage', '真实 Vue 3 + 存储'),
    ('Real Vue 3 + Style', '真实 Vue 3 + 样式'),
    ('Real Vue 3 + Theme', '真实 Vue 3 + 主题'),
    ('Real Vue 3 + TipTap', '真实 Vue 3 + TipTap'),
    ('Real Vue 3 + Type', '真实 Vue 3 + 类型'),
    ('Real Vue 3 + UI', '真实 Vue 3 + UI'),
    ('Real Vue 3 + UI-framework', '真实 Vue 3 + UI 框架'),
    ('Real Vue 3 + Upload', '真实 Vue 3 + 上传'),
    ('Real Vue 3 + Util', '真实 Vue 3 + 工具'),
    ('Real Vue 3 + Utility', '真实 Vue 3 + 工具'),
    ('Real Vue 3 + Validators', '真实 Vue 3 + 验证器'),
    ('Real Vue 3 + Virtual', '真实 Vue 3 + 虚拟'),
    ('Real Vue 3 + VirtualList', '真实 Vue 3 + 虚拟列表'),
    ('Real Vue 3 + Vue', '真实 Vue 3 + Vue'),
    ('Real Vue 3 + VxeTable', '真实 Vue 3 + VxeTable'),

    # Real Vue 3 + Theme
    ('Real Vue 3 + Theme.', '真实 Vue 3 + 主题。'),

    # Hook-level
    ('Real Vue 3 + Persisted Pinia.', '真实 Vue 3 + 持久化 Pinia。'),
    ('Real Vue 3 + Nitro mock-server.', '真实 Vue 3 + Nitro mock 服务端。'),
    ('Real Vue 3 + Nitro mock server.', '真实 Vue 3 + Nitro mock 服务端。'),
    ('Real Vue 3 + Mock Server.', '真实 Vue 3 + Mock 服务端。'),
    ('Real Vue 3 + Mock Server', '真实 Vue 3 + Mock 服务端'),

    # Real Vue 3 + various
    ('Real Vue 3 + Menu.', '真实 Vue 3 + 菜单。'),
    ('Real Vue 3 + Menu', '真实 Vue 3 + 菜单'),
    ('Real Vue 3 + i18n.', '真实 Vue 3 + i18n。'),
    ('Real Vue 3 + i18n', '真实 Vue 3 + i18n'),
    ('Real Vue 3 + UI Library.', '真实 Vue 3 + UI 库。'),
    ('Real Vue 3 + UI Library', '真实 Vue 3 + UI 库'),
    ('Real Vue 3 + UI library', '真实 Vue 3 + UI 库'),

    # Real Vue 3 + many
    ('Real Vue 3 + UI library.', '真实 Vue 3 + UI 库。'),
    ('Real Vue 3 + storage.', '真实 Vue 3 + 存储。'),
    ('Real Vue 3 + storage', '真实 Vue 3 + 存储'),
    ('Real Vue 3 +.', '真实 Vue 3。'),
    ('Real Vue 3 +', '真实 Vue 3 + '),

    # Real Vue 3
    ('Real Vue 3.', '真实 Vue 3。'),
    ('Real Vue 3', '真实 Vue 3'),

    # Real + Vue 3
    ('Real Vue 3 + Composables.', '真实 Vue 3 + 组合式函数。'),
    ('Real Vue 3 + Composables', '真实 Vue 3 + 组合式函数'),
    ('Real Vue 3 + Components.', '真实 Vue 3 + 组件。'),
    ('Real Vue 3 + Components', '真实 Vue 3 + 组件'),
    ('Real Vue 3 + Utility functions.', '真实 Vue 3 + 工具函数。'),
    ('Real Vue 3 + Utility functions', '真实 Vue 3 + 工具函数'),

    # Real + Vue 3
    ('Real Vue 3 + VbenForm.', '真实 Vue 3 + VbenForm。'),
    ('Real Vue 3 + VbenForm', '真实 Vue 3 + VbenForm'),
    ('Real Vue 3 + Tab.', '真实 Vue 3 + Tab。'),
    ('Real Vue 3 + Tab', '真实 Vue 3 + Tab'),
    ('Real Vue 3 + Style.', '真实 Vue 3 + 样式。'),
    ('Real Vue 3 + Style', '真实 Vue 3 + 样式'),
    ('Real Vue 3 + Tailwind utilities.', '真实 Vue 3 + Tailwind utility。'),
    ('Real Vue 3 + Tailwind utilities', '真实 Vue 3 + Tailwind utility'),
    ('Real Vue 3 + Toast.', '真实 Vue 3 + Toast。'),

    # Real Vue 3 + Icon
    ('Real Vue 3 + Icon.', '真实 Vue 3 + 图标。'),
    ('Real Vue 3 + Icon', '真实 Vue 3 + 图标'),
    ('Real Vue 3 + Icons.', '真实 Vue 3 + 图标。'),
    ('Real Vue 3 + Icons', '真实 Vue 3 + 图标'),

    # Real Vue 3 + Helpers
    ('Real Vue 3 + Helper Lib.', '真实 Vue 3 + Helper 库。'),
    ('Real Vue 3 + Helper Lib', '真实 Vue 3 + Helper 库'),
    ('Real Vue 3 + Hook.', '真实 Vue 3 + Hook。'),
    ('Real Vue 3 + Hook', '真实 Vue 3 + Hook'),

    # Layout / Layouts
    ('Real Vue 3 + Layout.', '真实 Vue 3 + 布局。'),
    ('Real Vue 3 + Layout', '真实 Vue 3 + 布局'),
    ('Real Vue 3 + Tree-shaking utilities.', '真实 Vue 3 + Tree-shaking utilities。'),

    # Pinia setup-style
    ('Real Vue 3 + Pinia setup-style store.', '真实 Vue 3 + Pinia setup 风格 store。'),
    ('Real Vue 3 + Pinia setup-style store', '真实 Vue 3 + Pinia setup 风格 store'),

    # Generic
    ('Real Vue 3 + Composition API.', '真实 Vue 3 + Composition API。'),
    ('Real Vue 3 + Composition API', '真实 Vue 3 + Composition API'),
    ('Real Vue 3 + Import', '真实 Vue 3 + Import'),
    ('Real Vue 3 + Importing', '真实 Vue 3 + Importing'),
    ('Real Vue 3 + Importing.', '真实 Vue 3 + Importing。'),

    # Special
    ('Real Vue 3 + JSX.', '真实 Vue 3 + JSX。'),
    ('Real Vue 3 + JSX', '真实 Vue 3 + JSX'),
    ('Real Vue 3 + Scrollbar.', '真实 Vue 3 + 滚动条。'),
    ('Real Vue 3 + Scrollbar', '真实 Vue 3 + 滚动条'),

    # Component definitions
    ('Real Vue 3 + Pinia typical Vue 3 demo.', '真实 Vue 3 + Pinia 典型 Vue 3 demo。'),
    ('Real Vue 3 + NProgress.', '真实 Vue 3 + NProgress。'),
    ('Real Vue 3 + NProgress', '真实 Vue 3 + NProgress'),
    ('Real Vue 3 + Notification.', '真实 Vue 3 + 通知。'),
    ('Real Vue 3 + Notification', '真实 Vue 3 + 通知'),
    ('Real Vue 3 + Overlay.', '真实 Vue 3 + 浮层。'),
    ('Real Vue 3 + Overlay', '真实 Vue 3 + 浮层'),

    # Vue 3 part translations
    ('Vue 3 + DatePicker', 'Vue 3 + 日期选择器'),
    ('Vue 3 + Descriptions', 'Vue 3 + 描述'),
    ('Vue 3 + Detail', 'Vue 3 + 详情'),
    ('Vue 3 + Dialog', 'Vue 3 + 对话框'),
    ('Vue 3 + Divider', 'Vue 3 + 分割线'),
    ('Vue 3 + Drawer', 'Vue 3 + 抽屉'),
    ('Vue 3 + Editable', 'Vue 3 + 可编辑'),
    ('Vue 3 + Empty', 'Vue 3 + 空'),
    ('Vue 3 + Form', 'Vue 3 + 表单'),

    # Misc English words that should be translated
    ('Plain English, JavaScript-free doc', '纯净英文，无 JavaScript 文档'),
    ('No JS', '无 JS'),
    ('No JS.', '无 JS。'),
    ('JS-free', '无 JS'),

    # 其他常用
    ('Use Vue 3 conventions.', '使用 Vue 3 约定。'),
    ('Use Vue 3 conventions', '使用 Vue 3 约定'),
    ('Vue 3 + typical Vue 3 demo.', 'Vue 3 + 典型 Vue 3 demo。'),
    ('Vue 3 + typical Vue 3 demo', 'Vue 3 + 典型 Vue 3 demo'),
    ('Vue 3 + Utility Helpers.', 'Vue 3 + 工具 Helpers。'),
    ('Vue 3 + Utility Helpers', 'Vue 3 + 工具 Helpers'),

    # 填补最后
    ('Vue 3 + Common UI.', 'Vue 3 + 通用 UI。'),
    ('Vue 3 + Common UI', 'Vue 3 + 通用 UI'),
    ('Vue 3 + Pre-Built.', 'Vue 3 + 预构建。'),
    ('Vue 3 + Pre-Built', 'Vue 3 + 预构建'),
    ('Vue 3 + Util ', 'Vue 3 + 工具 '),
    ('Vue 3 + Combination', 'Vue 3 + 组合'),
    ('Vue 3 + Auth.', 'Vue 3 + 认证。'),
    ('Vue 3 + Auth', 'Vue 3 + 认证'),

    # Real Vue 3 + Auth / Util
    ('Real Vue 3 + Auth.', '真实 Vue 3 + 认证。'),
    ('Real Vue 3 + Auth', '真实 Vue 3 + 认证'),
    ('Real Vue 3 + Util.', '真实 Vue 3 + 工具。'),
    ('Real Vue 3 + Util', '真实 Vue 3 + 工具'),
    ('Real Vue 3 + Helper.', '真实 Vue 3 + Helper。'),
    ('Real Vue 3 + Helper', '真实 Vue 3 + Helper'),

    # Last bit
    ('Vue 3 + Pure data.', 'Vue 3 + 纯数据。'),
    ('Vue 3 + Pure data', 'Vue 3 + 纯数据'),
    ('Vue 3 + Effective', 'Vue 3 + Effective'),
    ('Vue 3 + Vxe.', 'Vue 3 + Vxe。'),
    ('Vue 3 + Vxe', 'Vue 3 + Vxe'),

    # Real Vue 3 + shadcn/vue
    ('Real Vue 3 + shadcn-vue.', '真实 Vue 3 + shadcn-vue。'),
    ('Real Vue 3 + shadcn-vue', '真实 Vue 3 + shadcn-vue'),

    # misc
    ('Vue 3 + Tabs', 'Vue 3 + 标签页'),
    ('Vue 3 + Tag', 'Vue 3 + 标签'),
    ('Vue 3 + template management', 'Vue 3 + 模板管理'),
    ('Vue 3 + template', 'Vue 3 + 模板'),

    # Final random
    ('Vue 3 + ', 'Vue 3 + '),

    # Real Vue 3 + demos
    ('Real Vue 3 +', '真实 Vue 3 + '),

    # Real Vue 3 + final bits
    ('A Pinia store for managing', '用于管理...的 Pinia store'),
    ('A Pinia composable', '一个 Pinia 组合式函数'),
    ('A composable for managing', '用于管理...的组合式函数'),

    # Real Vue 3 + ts
    ('Real Vue 3 + ts.', '真实 Vue 3 + ts。'),
    ('Real Vue 3 + ts', '真实 Vue 3 + ts'),
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
