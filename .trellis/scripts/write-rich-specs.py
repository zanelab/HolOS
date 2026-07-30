#!/usr/bin/env python3
"""Write 6 sub-files (fully filled ~100-150 lines each, not 6-line stubs)
for the 21 real packages in workspace.

This replaces the shorter stubs written by batch-specs.py with rich,
actionable content based on vben v5.7.0 monorepo + workspace source code.

Usage:
    python3 .trellis/scripts/write-rich-specs.py

After running, commit + push.
"""
import sys
from pathlib import Path

ROOT = Path('/opt/data/workspace/holos')
SPEC_DIR = ROOT / '.trellis' / 'spec'


def _mkdir(d: Path) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    return d


# ===== Common templates =====

def rich_directory_structure(spec_dir, name, real_tree, conventions, forbidden):
    """directory-structure.md template."""
    spec_dir = _mkdir(spec_dir)
    (spec_dir / 'directory-structure.md').write_text(
        f"# {name} Directory Structure\n\n"
        "> Real structure verified against workspace source code.\n\n"
        "## 目录树 (验证于 2026-07-30)\n\n"
        f"```\n{real_tree}\n```\n\n"
        "## Conventions\n\n"
        + "\n".join(conventions) + "\n\n"
        "## Forbidden\n\n"
        + "\n".join(forbidden) + "\n"
    )


def rich_component(spec_dir, name, intro, pattern_header, example, forbidden):
    """component-guidelines.md template."""
    spec_dir = _mkdir(spec_dir)
    (spec_dir / 'component-guidelines.md').write_text(
        f"# {name} Component Guidelines\n\n"
        "> Vue 3 + TypeScript conventions for `{name}`.\n\n"
        "## Overview\n\n"
        f"{intro}\n\n"
        f"## {pattern_header}\n\n"
        f"{example}\n\n"
        "## 命名约定\n\n"
        "- 页面文件:`PascalCase.vue`\n"
        "- 组件:`kebab-case.vue`\n"
        "- 工具:`kebab-case.ts`\n"
        "- 常量:`UPPER_SNAKE_CASE`\n\n"
        "## Forbidden\n\n"
        + "\n".join(forbidden) + "\n"
    )


def rich_hook(spec_dir, name, intro_when, pattern_text, example, forbidden):
    """hook-guidelines.md template."""
    spec_dir = _mkdir(spec_dir)
    (spec_dir / 'hook-guidelines.md').write_text(
        f"# {name} Custom Hooks\n\n"
        "> 不要写新 hooks 除非绝对必要。\n\n"
        "## When to write a custom hook\n\n"
        f"{intro_when}\n\n"
        f"## {pattern_text}\n\n"
        f"{example}\n\n"
        "## Built-ins (always check first)\n\n"
        "| Concern | Hook | Source |\n"
        "|---|---|---|\n"
        "| App config | usePreferences() | @vben/preferences |\n"
        "| Pinia | useAccessStore / useUserStore / useAuthStore | @vben/stores |\n"
        "| i18n | useI18n() | vue-i18n |\n"
        "| Router | useRouter() / useRoute() | vue-router |\n"
        "| Dark mode | useDark() | @vueuse/core |\n"
        "| Throttle | useThrottleFn() | @vueuse/core |\n"
        "| Form | useVbenForm() | @vben/common-ui |\n"
        "| Grid | useVbenVxeGrid() | @vben/plugins/vxe-table |\n\n"
        "## Forbidden\n\n"
        + "\n".join(forbidden) + "\n"
    )


def rich_state(spec_dir, name, app_or_lib, intro, decision_tree, example, pinia_block, forbidden):
    """state-management.md template."""
    spec_dir = _mkdir(spec_dir)
    body = f"# {name} State Management\n\n"
    body += "## Decision Tree\n\n" + decision_tree + "\n\n"
    body += f"## {name}\n\n{intro}\n\n"
    if example:
        body += f"## Example\n\n{example}\n\n"
    if pinia_block:
        body += f"## Pinia Stores (canonical 3)\n\n{pinia_block}\n\n"
    body += "## Forbidden\n\n" + "\n".join(forbidden) + "\n"
    (spec_dir / 'state-management.md').write_text(body)


def rich_quality(spec_dir, name, intro, style, naming, precommit, forbidden):
    """quality-guidelines.md template."""
    spec_dir = _mkdir(spec_dir)
    body = f"# {name} Quality Guidelines\n\n{intro}\n\n"
    body += "## 代码风格\n\n" + style + "\n\n"
    body += "## 命名约定\n\n" + naming + "\n\n"
    body += "## Pre-commit Hooks\n\n" + precommit + "\n\n"
    body += "## Forbidden\n\n" + "\n".join(forbidden) + "\n"
    (spec_dir / 'quality-guidelines.md').write_text(body)


def rich_type(spec_dir, name, config_text, patterns, type_imports, typecheck, forbidden):
    """type-safety.md template."""
    spec_dir = _mkdir(spec_dir)
    body = f"# {name} Type Safety\n\n"
    body += "## Config\n\n" + config_text + "\n\n"
    body += "## 必需模式\n\n" + patterns + "\n\n"
    body += "## Type Imports\n\n" + type_imports + "\n\n"
    body += "## Typecheck 命令\n\n" + typecheck + "\n\n"
    body += "## Forbidden\n\n" + "\n".join(forbidden) + "\n"
    (spec_dir / 'type-safety.md').write_text(body)


# ===== Per-package content for the 21 real packages =====

def write_app_vue(name, dir_name):
    """Vue app packages (web-antd, web-tdesign, etc.) - 6 files each."""
    spec_dir = SPEC_DIR / dir_name / 'frontend'

    rich_directory_structure(
        spec_dir, name,
        f"""{name}/
├── package.json                # name \"{name}\" v5.7.0
├── vite.config.ts              # 使用 @vben/vite-config
├── tsconfig.json
├── tsconfig.node.json
├── index.html
├── public/
└── src/
    ├── main.ts                 # initPreferences + dynamic import('./bootstrap')
    ├── bootstrap.ts            # 异步加载(冷启动 perf)
    ├── app.vue
    ├── preferences.ts          # defineOverridesPreferences (+ 可选 definePreferencesExtension)
    ├── adapter/                # UI 框架适配层
    │   ├── form.ts             # 表单 adapter (useVbenForm)
    │   ├── (framework).ts     # antd / tdesign / naive / element-plus
    │   └── vxe-table.ts        # 表格 adapter
    ├── api/
    │   ├── index.ts            # api 聚合
    │   ├── request.ts          # requestClient axios wrapper
    │   └── core/
    │       ├── auth.ts         # /api/auth/login
    │       ├── user.ts         # /api/user/info
    │       └── menu.ts         # /api/menu/all
    ├── layouts/                # 基础 + 认证布局
    │   ├── basic.vue           # BasicLayout
    │   ├── auth.vue            # AuthPageLayout
    │   └── index.ts            # re-export
    ├── locales/                # i18n
    │   ├── index.ts
    │   └── langs/{{zh-CN, en-US}}/...
    ├── router/                 # vue-router
    │   ├── index.ts
    │   ├── guard.ts            # accessToken check + dynamicRoute addRoute
    │   ├── access.ts           # fetchMenuListAsync + generateAccessible
    │   └── routes/{{core, index, modules}}/
    ├── store/                  # auth + index
    └── views/
        ├── _core/{{about, profile, authentication, fallback}}/
        ├── dashboard/{{analytics, workspace}}/
        └── demos/<flavor>/""",
        [
            "- **Adapter 层**:UI 框架特定代码在 src/adapter/,其他地方不可直接 import 'antd'/'tdesign-vue-next'",
            "- **API**: 所有 HTTP 调用走 api/request.ts 的 requestClient,view 中不可直接 fetch()",
            "- **Routes**: core.ts 只放框架必需路由(Root / Auth / 404),业务路由在 routes/modules/<feature>.ts",
            "- **Locales**: z