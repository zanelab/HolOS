# @vben/utils Directory Structure

> Real layout for `packages/utils/`. Source verified 2026-07-30.

## Purpose

`@vben/utils` is the workspace's **app-level utility package**. It hosts
the route/menu helpers (`generateMenus`, `findMenuByPath`,
`generateRoutesBackend`, `generateRoutesFrontend`, `mergeRouteModules`,
`resetRoutes`) and the DOM/UI helpers (`getPopupContainer`,
`unmountGlobalLoading`). It also re-exports the deeper `@vben-core/shared/*`
modules (`cache`, `color`, `utils`).

## 目录树 (verified from `packages/utils/`)

```
@vben/utils/                        # workspace: packages/utils/
├── package.json                    # name "@vben/utils" v5.7.0
├── tsconfig.json                   # extends @vben/tsconfig/library.json
└── src/
    ├── index.ts                    # public barrel
    └── helpers/
        ├── index.ts                # re-exports all helpers
        ├── find-menu-by-path.ts    # findMenuByPath, findRootMenuByPath
        ├── generate-menus.ts       # generateMenus(routes, router)
        ├── generate-routes-backend.ts
        ├── generate-routes-frontend.ts
        ├── get-popup-container.ts  # DOM portal anchor
        ├── merge-route-modules.ts  # dynamic route merge
        ├── reset-routes.ts         # resetStaticRoutes(router, routes)
        ├── unmount-global-loading.ts
        └── __tests__/
```

## Public barrel (verified)

```ts
// packages/utils/src/index.ts
export * from './helpers';
export * from '@vben-core/shared/cache';
export * from '@vben-core/shared/color';
export * from '@vben-core/shared/utils';
```

## Real helper (verified)

```ts
// packages/utils/src/helpers/find-menu-by-path.ts
import type { MenuRecordRaw } from '@vben-core/typings';

function findMenuByPath(
  list: MenuRecordRaw[],
  path?: string,
): MenuRecordRaw | null {
  for (const menu of list) {
    if (menu.path === path) {
      return menu;
    }
    const findMenu = menu.children && findMenuByPath(menu.children, path);
    if (findMenu) {
      return findMenu;
    }
  }
  return null;
}

export { findMenuByPath, findRootMenuByPath };
```

## Conventions

- **Helpers directory** — `helpers/<name>.ts` per utility.
- **Pure functions** — no Vue runtime, no Pinia.
- **Re-exports of `@vben-core/shared/*`** — local cache + color + utils.
- **Type imports** — `import type { MenuRecordRaw, RouteRecordRaw }` etc.
- **Tree-shake friendly** — named exports only.
- **Tests** live in `helpers/__tests__/`.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Helper file | `kebab-case.ts` | `find-menu-by-path.ts` |
| Function | `camelCase` verb-first | `findMenuByPath`, `generateMenus` |
| Type | `PascalCase` | `RouteModuleType` |
| Re-export | `export * from '...'` | `export * from './helpers';` |

## Forbidden

- ❌ 不要 add Vue components — pure functions only
- ❌ 不要 put Pinia stores here — wrong layer
- ❌ 不要 add class definitions — keep functions pure
- ❌ 不要 bypass `@vben-core/shared/utils` for tree helpers — reuse
- ❌ 不要 add i18n strings — utility layer
- ❌ 不要 store state in a module-level variable — pure functions
- ❌ 不要 reach into DOM outside of `getPopupContainer` / `unmountGlobalLoading`
