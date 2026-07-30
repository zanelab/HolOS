#!/usr/bin/env python3
"""Pass 4 translation: Common English prose phrases frequently appearing
in spec files (headers, sentences, bullet points, table column headers).

Builds on translate-specs.py + translate-specs2.py + translate-deep.py.
"""
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_DIR = ROOT / '.trellis' / 'spec'

TRANSLATIONS = [
    # ===== Short phrases / single words =====
    ('Real Vue 3', '真实 Vue 3'),
    ('Vue 3 conventions', 'Vue 3 约定'),
    ('Vue 3 Conventions', 'Vue 3 约定'),
    ('Vue 3 conventions.', 'Vue 3 约定。'),
    ('Vue 3 Types', 'Vue 3 类型'),
    ('Vue 3 + Types', 'Vue 3 + 类型'),
    ('Vue 3 + Helper Lib conventions for', 'Vue 3 + Helper 库约定：'),
    ('Vue 3 + Helper Lib conventions', 'Vue 3 + Helper 库约定'),
    ('Vue 3 + Helper Lib', 'Vue 3 + Helper 库'),

    # Component / Hooks / State generic
    ('Self-contained', '自包含'),
    ('A real', '真实的'),
    ('A typical', '典型的'),
    ('a small', '一个小的'),
    ('A small', '一个小的'),
    ('a typical', '一个典型的'),
    ('A typical', '一个典型的'),
    ('a minimal', '一个最小化的'),
    ('A minimal', '一个最小化的'),

    # "Pure X" common
    ('a pure', '一个纯'),
    ('A pure', '一个纯'),
    ('a composable', '一个组合式函数'),
    ('A composable', '一个组合式函数'),
    ('an', '一个'),
    ('A ', '一个'),

    # Critical "is" phrases
    (' is ', ' 是 '),
    (' are ', ' 是 '),
    ('was', '是'),
    (' were ', ' 是 '),
    (' be ', '是'),

    # Phrases from existing files
    ('Tailwind utilities', 'Tailwind utility 类'),
    ('Tailwind utility', 'Tailwind utility'),
    ('tags:', '标签：'),
    ('Tags:', '标签：'),

    # "Section X" style
    ('Section 1', '一节'),
    ('Section 2', '二节'),
    ('section 1', '一节'),
    ('section 2', '二节'),

    # Common sections
    ('## Sections', '## 章节'),
    ('Section', '章节'),

    # Common "verbose" phrases
    ('see ', '见 '),
    ('See ', '见 '),
    ('for more', '更多'),
    ('For more', '更多'),

    # Misc
    (' Specifically,', '具体来说，'),
    ('Specifically,', '具体来说，'),
    ('In particular', '特别是'),
    ('for example', '例如'),
    ('For example', '例如'),

    # Lots of small fixups
    ('real-world', '真实'),
    ('real ', '真实 '),
    ('real', '真实'),
    ('real.', '真实.'),

    # How is it implemented
    ('implemented', '实现'),
    ('Implementation', '实现'),
    ('implementation', '实现'),

    # Description
    (' Description', ' 描述'),
    (' description', ' 描述'),

    # Misc
    ('A simple example', '简单示例'),
    ('Simple example', '简单示例'),

    # Common
    ('Hello world', 'Hello world'),
    ('here', '此处'),
    ('Here', '此处'),
    (' above', ' 上方'),
    (' below', ' 下方'),

    # Generic
    ('Please note', '请注意'),
    ('note that', '请注意'),
    ('Note that', '请注意'),

    # Final "Rules" cleanup
    ('see also', '另见'),
    ('See also', '另见'),

    # "It" / "This" pronouns
    ('It is', '这是'),
    ('it is', '这是'),
    ('This is', '这是'),
    ('this is', '这是'),
    ('that is', '即'),

    # Fill comments
    (' Documentation', ' 文档'),
    ('Documentation', '文档'),
    ('documentation', '文档'),

    # "Available" etc
    ('Available', '可用'),
    ('available', '可用'),

    # Runtime
    ('runtime', '运行时'),
    ('Runtime', '运行时'),

    # Misc
    ('full', '完整'),
    ('Full', '完整'),
    ('with no', '无'),
    (' consistent', ' 一致'),
    (' consistent.', ' 一致。'),

    # "Self-X" patterns
    ('Self', '自身'),
    ('self', '自身'),

    # Common
    (' Basic', '基础'),
    ('basic', '基础'),

    # Generic
    (' we ', '我们'),
    (' we.', '我们。'),

    # "you" / "your"
    (' you', '你'),
    (' your', '你的'),
    ('You', '你'),
    ('Your', '你的'),

    # Anything "of"
    (' of ', '的'),

    # Final tail
    ('Todos', '待办'),
    ('todos', '待办'),
    ('changelog', '变更日志'),
    ('CHANGELOG', '变更日志'),

    # Misc fragments
    ('Live example', '在线示例'),
    ('cookbook', '指南'),
    ('Cookbook', '指南'),
    ('Locale X', '本地化 X'),

    # Bigger phrases
    ('free, open source', '免费，开源'),

    # Final tail: common styles
    ('A demo', 'Demo'),
    (' a demo', ' Demo'),
    (' A demo', ' Demo'),
    (' demo', ' Demo'),

    # Generics
    (' in production', ' 生产环境'),
    ('In production', '生产环境'),

    # Build
    (' build', ' 构建'),
    (' Build', ' 构建'),
    ('Compile', '编译'),
    (' compile', ' 编译'),
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
