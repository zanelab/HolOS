# @vben/constants Directory Structure

> Real layout for `packages/constants/`. Source verified 2026-07-30.

## 目录树 (实际)

```
@vben/constants/                    # workspace: packages/constants/
├── package.json                    # name "@vben/constants" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
└── src/
    ├── index.ts                    # 公开 barrel — re-exports 全部
    ├── core.ts                     # 核心常量 (LOGIN_PATH, HOME_PATH, ...)
    └── (additional module files)
```

## 实际源码参考

`packages/constants/src/core.ts` (实际内容):

```ts
// packages/constants/src/core.ts (verified)
export const LOGIN_PATH = '/auth/login';
export const HOME_PATH = '/dashboard';
export const APP_NAME_DEFAULT = 'Vben Admin';

export type LayoutType =
  | 'full-content'
  | 'header-mixed-nav'
  | 'header-nav'
  | 'header-sidebar-nav'
  | 'mixed-nav'
  | 'sidebar-mixed-nav'
  | 'sidebar-nav';
```

## Conventions

- **公开 barrel** `src/index.ts` re-exports 全部 members
- **纯值 + types**,no IO
- **Tree-shake friendly** — 每个 const / type 独立命名导出
- **零运行时依赖** — 不引入第三方 npm 包
- **side-effect-free imports**

## 常用 Consumers

| 谁用 | 怎么用 |
|---|---|
| `@vben/preferences` | `import { LOGIN_PATH, HOME_PATH } from '@vben/constants'` |
| `@vben/router/guard.ts` (各 app) | `import { LOGIN_PATH } from '@vben/constants'` 决定 redirect |
| `@vben/stores` | 类型上用 `LOGIN_PATH` 决定默认值 |

## Forbidden

- ❌ 不要添加 IO function(网络调用 / 文件操作)
- ❌ 不要添加 Vue refs / Pinia stores — 这是纯数据
- ❌ 不要把 const 打包进 namespace / class(牺牲 tree-shaking)
- ❌ 不要在 `core.ts` 加 业务相关常量 — 那些是 app 本地常量
- ❌ 不要引入其他 `@vben/*` packages — 这必须是 leaf package
