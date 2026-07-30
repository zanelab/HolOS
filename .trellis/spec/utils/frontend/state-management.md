# @vben/utils State Management

> Stateless helpers. Values flow through arguments and returns.

## Purpose

`@vben/utils` holds no reactive state. The package is a collection of
**pure functions** whose outputs depend strictly on inputs. State lives
in `@vben/stores` (Pinia) and `@vben/preferences` (singleton).

## Stateless helpers

```ts
// packages/utils/src/helpers/find-menu-by-path.ts (verified)
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
```

No `ref`, no `reactive`, no `defineStore`.

## Stateful side-effects (DOM-targeted)

Two helpers touch the DOM directly, but they are **side-effect loaded
once** — no internal state:

```ts
// packages/utils/src/helpers/unmount-global-loading.ts
export function unmountGlobalLoading() {
  const el = document.querySelector('#app-loading');
  if (el) {
    el.remove();
  }
}
```

```ts
// packages/utils/src/helpers/get-popup-container.ts
export function getPopupContainer(triggerEl?: HTMLElement): HTMLElement {
  return triggerEl?.parentElement ?? document.body;
}
```

## Re-exported shared utils

```ts
// packages/utils/src/index.ts (verified)
export * from './helpers';
export * from '@vben-core/shared/cache';
export * from '@vben-core/shared/color';
export * from '@vben-core/shared/utils';
```

`@vben-core/shared/utils` includes `createStack`, `openWindow`, and tree
ops. These are also pure (except `createStack` which returns a stateful
object — still scoped to the caller).

## State surface map

| Surface | Type | Owned by |
|---|---|---|
| `preferences` | `reactive<Preferences>` | `@vben/preferences` |
| Pinia stores | `defineStore` | `@vben/stores` |
| `i18n.global` | `Ref<Locale>` | `@vben/locales` |
| Helpers | pure functions | `@vben/utils` |

## Conventions

- **Pure functions** — same input ⇒ same output.
- **No module-level mutable vars** — `let pinia: Pinia` is a NO here.
- **Side-effect helpers** (`unmountGlobalLoading`, `getPopupContainer`)
  are scoped to UI boot.
- **Tree helpers** (`mapTree`, `filterTree`, `sortTree`) are pure and
  re-exported from `@vben-core/shared/utils`.
- **`createStack` returns a new instance** — never singleton.

## Naming

| Thing | Convention | Example |
|---|---|---|
| Pure helper | `verbXxx` | `findMenuByPath`, `generateMenus` |
| Side-effect async | `unmountXxx` | `unmountGlobalLoading` |
| DOM query | `getXxx` | `getPopupContainer` |
| Reset | `resetXxx` | `resetStaticRoutes` |

## Forbidden

- ❌ 不要 create a Pinia store here — wrong layer
- ❌ 不要 add `ref`/`reactive` to a helper file — pure functions
- ❌ 不要 hold module-level variables — pure functions
- ❌ 不要 subscribe to Pinia state from helpers — pass it in
- ❌ 不要 cache results in module scope — call sites decide
- ❌ 不要 make `getPopupContainer` async — it's DOM-only
- ❌ 不要 import `@vben/stores` or `@vben/preferences` here — circular
