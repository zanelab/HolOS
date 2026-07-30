# @vben/utils Hook Guidelines

> No `useXxx()` in this package. Apps compose helpers into hooks.

## Purpose

`@vben/utils` does not define composables. Vue hooks that **use** these
helpers live in `@vben/hooks` and `@vben-core/composables`. This file
documents the bind patterns so apps know how to wrap helpers into a
composable.

## Re-exported composables from `@vben-core/shared/utils`

`@vben/utils` re-exports `*` from `@vben-core/shared/utils`, which
includes:

- `mapTree`, `filterTree`, `sortTree`, `traverseTreeValues` — tree ops
- `merge`, `clone`, `diff` — object helpers
- `openWindow`, `startProgress`, `stopProgress` — UI helpers
- `createStack` — LIFO stack data structure

```ts
// apps/web-antdv-next/src/store/auth.ts (real)
import { createStack } from '@vben/utils';
const visitHistory = createStack<string>();
```

## Hook that wraps a helper

```ts
// apps/web-antdv-next/src/composables/use-menu.ts (real pattern)
import { findMenuByPath } from '@vben/utils';
import { useAccessStore } from '@vben/stores';

export function useMenu() {
  const accessStore = useAccessStore();
  function currentMenu(path: string) {
    return findMenuByPath(accessStore.accessMenus, path);
  }
  return { currentMenu };
}
```

## Hook that wraps a route helper

```ts
// apps/web-antdv-next/src/composables/use-reset-routes.ts
import { resetStaticRoutes } from '@vben/utils';
import { useRouter } from 'vue-router';

export function useResetRoutes() {
  const router = useRouter();
  return () => resetStaticRoutes(router, router.options.routes);
}
```

## Hook that wraps a UI helper

```ts
// apps/web-antdv-next/src/composables/use-popup-container.ts
import { getPopupContainer } from '@vben/utils';
import { computed, ref, type Ref } from 'vue';

export function usePopupContainer(target: Ref<HTMLElement | undefined>) {
  return computed(() => getPopupContainer(target.value));
}
```

## Conventions

- **No `useXxx()` exports in this package** — pure functions only.
- **Composable wrappers** live in `@vben/hooks` or app-local
  `composables/` folder.
- **Hooks reuse helpers** — never duplicate their logic.
- **Hooks return refs/computed** — helpers return values.
- **No `onMounted`/`watch` inside helpers** — sync only.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Helper | `verbXxx` | `findMenuByPath` |
| Composable wrapper | `useXxx` | `useMenu`, `useResetRoutes` |
| Ref param | `Ref<HTMLElement | undefined>` | — |
| Computed return | `ComputedRef<...>` | — |

## Forbidden

- ❌ 不要 export `useXxx()` from `@vben/utils` — pure functions only
- ❌ 不要 add `onMounted`/`watch` inside helpers — sync only
- ❌ 不要 couple helpers to a specific component shape
- ❌ 不要 use `ref`/`reactive` inside helpers — wrap in composables
- ❌ 不要 depend on Pinia / vue-router inside `@vben/utils` — pass them in
- ❌ 不要 call `useRouter()` inside this package — passed by caller
- ❌ 不要 add `try/catch` for control flow — let errors propagate
