# @vben/utils Component Guidelines

> No Vue components. Vue files in this package would be a red flag.

## Purpose

`@vben/utils` ships only pure helpers. Vue components live in
`@vben-core/common-ui`, `@vben-core/ui-kit`, and per-app folders. This
package provides the **traffic-cop functions** that components call to
resolve menus, manage routes, and anchor popups.

## Recommended: pure helpers only

```ts
// apps/web-antdv-next/src/router/index.ts (real)
import { resetStaticRoutes } from '@vben/utils';

const resetRoutes = () => resetStaticRoutes(router, routes);
```

## Menu composition

```ts
// apps/web-antdv-next/src/store/auth.ts (real pattern)
import { findMenuByPath } from '@vben/utils';

const menu = findMenuByPath(accessStore.accessMenus, currentPath);
```

## Anchor for popup containers

```vue
<!-- apps/web-antdv-next/src/views/demos/forms/index.vue (real pattern) -->
<script setup lang="ts">
import { getPopupContainer } from '@vben/utils';

const wrapperRef = ref<HTMLDivElement>();
const container = computed(() => getPopupContainer(wrapperRef.value));
</script>

<template>
  <div ref="wrapperRef">
    <Select :get-popup-container="container" />
  </div>
</template>
```

## Unmount global loading

```ts
// apps/web-antdv-next/src/main.ts (real)
import { unmountGlobalLoading } from '@vben/utils';

// 在初始化完成后调用
initApplication().finally(() => {
  unmountGlobalLoading();
});
```

## Real route reset

```ts
// packages/utils/src/helpers/reset-routes.ts (verified)
export function resetStaticRoutes(
  router: Router,
  routes: RouteRecordRaw[],
): void {
  const staticRouteNames = traverseTreeValues<
    RouteRecordRaw,
    RouteRecordName | undefined
  >(routes, (route) => route.name);

  const { getRoutes, hasRoute, removeRoute } = router;
  const allRoutes = getRoutes();
  allRoutes.forEach(({ name }) => {
    if (name && !staticRouteNames.includes(name) && hasRoute(name)) {
      removeRoute(name);
    }
  });
}
```

## Conventions

- **Helpers are pure** — no side effects beyond DOM-targeted ones
  (`getPopupContainer`, `unmountGlobalLoading`).
- **Re-exports** from `@vben-core/shared/*` are part of the public surface.
- **Helpers accept their dependencies** — `generateMenus(routes, router)`.
- **No Vue reactivity exposed** — components wrap with `computed`/`watch`.
- **No `defineComponent` definitions** here.
- **No JSX** — stick to TS.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Function | `verbXxx` | `findMenuByPath`, `generateMenus` |
| Dom anchor | `getPopupContainer(el)` | — |
| Loader | `unmountGlobalLoading()` | — |
| Route helper | `resetStaticRoutes(router, routes)` | — |
| Module helper | `mergeRouteModules(routeModules)` | — |

## Forbidden

- ❌ 不要 add `.vue` files to this package — wrong layer
- ❌ 不要 write `defineComponent` here — pure functions
- ❌ 不要 couple helpers to a specific UI framework — keep generic
- ❌ 不要 reach into `document.body` directly — use `getPopupContainer`
- ❌ 不要 add `localStorage` reads outside the cache helper
- ❌ 不要 return `Promise<void>` from sync helpers — sync only
- ❌ 不要 mutate the input parameters — pure functions
- ❌ 不要 throw untyped errors — extend `Error` subclasses
