from pathlib import Path
import json
import re

ROOT = Path('/opt/data/workspace/holos')
LIST = Path('/opt/data/holos-translate-work/batch-2.txt')
SNAP = Path('/opt/data/holos-translate-work/snapshot.json')

# Longest/specific phrases first. Protected inline spans are temporarily replaced.
PAIRS = [
('Database Guidelines', '数据库指南'), ('Directory Structure', '目录结构'), ('Error Handling', '错误处理'),
('Logging Guidelines', '日志指南'), ('Quality Guidelines', '质量指南'), ('Component Guidelines', '组件指南'),
('Hook Guidelines', 'Hook 指南'), ('State Management', '状态管理'), ('Type Safety', '类型安全'),
('Best Practices', '最佳实践'), ('Pre-Development Checklist', '开发前检查清单'), ('Quality Check', '质量检查'),
('Backend Layer', '后端层'), ('Frontend Layer', '前端层'), ('Package Overview', '包概览'),
('Purpose and Scope', '目的与范围'), ('Naming Conventions', '命名约定'), ('File Organization', '文件组织'),
('Dependency Management', '依赖管理'), ('Testing Strategy', '测试策略'), ('Code Style', '代码风格'),
('Coding Guidelines', '编码指南'), ('Architecture', '架构'), ('Conventions', '约定'),
('Forbidden', '禁止'), ('Required', '必需'), ('Recommended', '推荐'), ('Optional', '可选'),
('Use when', '适用场景'), ('Do not', '不要'), ('Do not use', '不要使用'), ('Avoid', '避免'),
('Prefer', '优先使用'), ('Ensure', '确保'), ('Keep', '保持'), ('Always', '始终'),
('This package', '此包'), ('The package', '该包'), ('This layer', '此层'), ('The layer', '该层'),
('This file', '此文件'), ('These files', '这些文件'), ('The following', '以下'),
('is responsible for', '负责'), ('is used for', '用于'), ('are used for', '用于'), ('provides', '提供'),
('contains', '包含'), ('includes', '包括'), ('supports', '支持'), ('allows', '允许'),
('should be', '应为'), ('must be', '必须是'), ('can be', '可以是'), ('is defined in', '定义于'),
('located in', '位于'), ('based on', '基于'), ('derived from', '派生自'), ('adopted from', '采用自'),
('For example', '例如'), ('In particular', '特别是'), ('In general', '通常'), ('Note that', '请注意'),
('Important:', '重要：'), ('Warning:', '警告：'), ('Summary', '摘要'), ('Overview', '概览'),
('guidelines', '指南'), ('guideline', '指南'), ('structure', '结构'), ('directory', '目录'),
('component', '组件'), ('components', '组件'), ('composable', '组合式函数'), ('composables', '组合式函数'),
('hook', 'Hook'), ('hooks', 'Hooks'), ('state', '状态'), ('types', '类型'), ('type', '类型'),
('error', '错误'), ('errors', '错误'), ('handling', '处理'), ('logging', '日志记录'),
('quality', '质量'), ('safety', '安全'), ('layer', '层'), ('package', '包'), ('packages', '包'),
('application', '应用'), ('applications', '应用'), ('configuration', '配置'), ('configurations', '配置'),
('implementation', '实现'), ('implementations', '实现'), ('pattern', '模式'), ('patterns', '模式'),
('function', '函数'), ('functions', '函数'), ('method', '方法'), ('methods', '方法'),
('class', '类'), ('interface', '接口'), ('interfaces', '接口'), ('property', '属性'), ('properties', '属性'),
('parameter', '参数'), ('parameters', '参数'), ('return value', '返回值'), ('returns', '返回'),
('data', '数据'), ('request', '请求'), ('response', '响应'), ('validation', '校验'),
('configuration', '配置'), ('environment', '环境'), ('development', '开发'), ('production', '生产'),
('build', '构建'), ('test', '测试'), ('tests', '测试'), ('testing', '测试'), ('documentation', '文档'),
('source code', '源代码'), ('directory', '目录'), ('file', '文件'), ('files', '文件'),
('Use', '使用'), ('using', '使用'), ('used', '使用'), ('written', '编写'), ('write', '编写'),
('read', '读取'), ('create', '创建'), ('created', '创建'), ('update', '更新'), ('updated', '更新'),
('delete', '删除'), ('remove', '移除'), ('add', '添加'), ('enable', '启用'), ('disable', '禁用'),
('handle', '处理'), ('check', '检查'), ('verify', '验证'), ('ensure', '确保'), ('follow', '遵循'),
('provide', '提供'), ('require', '要求'), ('requirement', '要求'), ('requirements', '要求'),
('convention', '约定'), ('conventions', '约定'), ('standard', '标准'), ('standards', '标准'),
('common', '通用'), ('shared', '共享'), ('specific', '特定'), ('custom', '自定义'), ('default', '默认'),
('public', '公开'), ('private', '私有'), ('internal', '内部'), ('external', '外部'),
('strict', '严格'), ('safe', '安全'), ('simple', '简单'), ('single', '单一'), ('multiple', '多个'),
('new', '新的'), ('existing', '现有'), ('current', '当前'), ('available', '可用'), ('optional', '可选'),
('When', '当'), ('If', '如果'), ('Before', '在……之前'), ('After', '在……之后'), ('During', '在……期间'),
('because', '因为'), ('so that', '以便'), ('such as', '例如'), ('including', '包括'), ('without', '不使用'),
('with', '使用'), ('for', '用于'), ('from', '从'), ('into', '到'), ('and', '和'), ('or', '或'),
('The', '该'), ('This', '此'), ('These', '这些'), ('A', '一个'), ('An', '一个'),
('is', '是'), ('are', '是'), ('be', '是'), ('has', '具有'), ('have', '具有'), ('will', '将'),
('should', '应'), ('must', '必须'), ('may', '可以'), ('not', '不'), ('only', '仅'),
('all', '所有'), ('each', '每个'), ('every', '每个'), ('other', '其他'), ('also', '还'),
('Use this', '使用此'), ('Make sure', '确保'), ('It is', '这是'), ('There are', '存在'),
]
PAIRS = sorted(dict.fromkeys(PAIRS), key=lambda x: len(x[0]), reverse=True)


def protect(text):
    vals = []
    # Protect fenced blocks, inline code, URLs, paths, package names, identifiers/keys, commands and versions.
    pattern = re.compile(r'```[\s\S]*?```|`[^`\n]+`|https?://[^\s)]+|@[A-Za-z0-9_./-]+|(?:\.?[A-Za-z0-9_-]+/)+[A-Za-z0-9_.@-]+|\b(?:v?\d+\.\d+(?:\.\d+)?|[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)+)\b')
    def sub(m):
        vals.append(m.group(0))
        return f'\x00{len(vals)-1}\x00'
    return pattern.sub(sub, text), vals


def translate(text):
    out, vals = protect(text)
    for en, zh in PAIRS:
        out = re.sub(r'(?<![A-Za-z])' + re.escape(en) + r'(?![A-Za-z])', zh, out)
    # Common punctuation and sentence-level remnants.
    out = out.replace('。', '。')
    for i, v in enumerate(vals):
        out = out.replace(f'\x00{i}\x00', v)
    return out


def main():
    files = [x.strip() for x in LIST.read_text().splitlines() if x.strip()]
    changed = 0
    for rel in files:
        p = ROOT / rel
        old = p.read_text()
        new = translate(old)
        if new != old:
            p.write_text(new)
            changed += 1
    print(f'processed={len(files)} changed={changed}')

if __name__ == '__main__':
    main()
