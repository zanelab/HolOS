# menu-ui — PLACEHOLDER SPEC

**Expected package:** `@vben-core/menu-ui` — Menu UI — sidebar menu items, submenu, breadcrumb, menu-folder, menu-collapse, search panel. Pure render, no data fetching.

> ⚠️ **PLACEHOLDER DOCS** — This package does **not** exist in the current
> workspace. The structure, conventions, and code examples below are
> best-guess projections based on the upstream `vben v5.7.0` monorepo
> (`vbenjs/vben-admin-monorepo`) and the role this package plays
> in a real vben app. **Replace this file with real content when (and
> only when) the corresponding `packages/menu-ui/`
> directory lands upstream.**

Do **not** implement against this placeholder — code that imports from
`@vben-core/menu-ui` will fail to typecheck.
## Where composables live

- **Pure utilities** (`useScroll`, `useScrollbar`, `useElementVisibility`)
  → `@vben/composables` — **stateless**, no preferences, no stores.
- **App-aware composables** (`useAppTheme`, `useAppMenu`, `useAppTabbar`)
  → `@vben/hooks` — may depend on `@vben/preferences`, `@vben/stores`.
- **UI-coupled composables** (`useVbenForm`, `useVbenModal`)
  → `@vben-core/menu-ui` — colocated with their components.

## Conventions

- **File** `use-<feature>.ts` — kebab-case prefix, one hook per file.
- **Export** named export only: `export function useScroll(…) { … }`.
- **Return shape** — plain object with refs + helpers (no class).
- **Inputs** accept `MaybeRefOrGetter<T>` so callers can pass refs/getters
  without `.value`.
- **Cleanup** — every `addEventListener` / `watch` / `setInterval`
  registers a `onScopeDispose(() => …)` to avoid leaks.
- **Naming** — never collide with `vueuse`; if you need a vueuse function,
  re-export it under a clearer name from `@vben-core/menu-ui` instead of
  re-implementing.

## Real-style code example (≥10 lines)

```ts
import { onMounted, onScopeDispose, ref, toValue, watch, type MaybeRefOrGetter } from 'vue';

export interface UseScrollOptions {
  target?: MaybeRefOrGetter<HTMLElement | Window | null>;
  threshold?: number;
  onScroll?: (y: number) => void;
}

export function useScroll(options: UseScrollOptions = {}) {
  const y = ref(0);
  const el = () => toValue(options.target) ?? window;
  function handler() {
    const t = el() as HTMLElement | Window;
    y.value = 'scrollY' in t ? t.scrollY : (t as HTMLElement).scrollTop;
    options.onScroll?.(y.value);
  }
  onMounted(() => el()?.addEventListener('scroll', handler, { passive: true }));
  watch(el, (n, o) => {
    o?.removeEventListener('scroll', handler);
    n?.addEventListener('scroll', handler, { passive: true });
  });
  onScopeDispose(() => el()?.removeEventListener('scroll', handler));
  return { y };
}
```

## Built-ins (always prefer these — re-export, don't re-implement)

| Concern | Hook | Source |
|---|---|---|
| Window scroll | `useWindowScroll` | `@vueuse/core` |
| Scrollbar width | `useScrollbar` | `@vueuse/core` |
| Element visibility | `useElementVisibility` | `@vueuse/core` |
| App theme | `useAppTheme()` | `@vben/hooks` |
| User store | `useUserStore()` | `@vben/stores` |

## Forbidden

- ❌ Don't put pure business logic in a composable — that lives in
  `src/utils/` and gets wrapped by the composable.
- ❌ Don't reach for `document.querySelector` inside composables —
  accept the target element via `MaybeRefOrGetter`.
- ❌ Don't return Vue `ref`s from helpers that aren't hooks (helpers
  belong in `@vben/utils`).
- ❌ Don't shadow `useXxx` names from `@vueuse/core` — re-export them
  with a more specific name.
- ❌ Don't add side effects at module top-level (e.g. global
  `addEventListener`) — all side effects must be inside the hook body.
- ❌ Don't call `useXxx` outside `<script setup>` or another `setup()`.
