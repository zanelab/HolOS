# composables — PLACEHOLDER SPEC

**Expected package:** `@vben/composables` — Pure Vue 3 composables — `useScroll`, `useScrollbar`, `useElementVisibility`, `useIntersectionObserver`, `useVModel` etc. Tree-shake friendly.

> ⚠️ **PLACEHOLDER DOCS** — This package does **not** exist in the current
> workspace. The structure, conventions, and code examples below are
> best-guess projections based on the upstream `vben v5.7.0` monorepo
> (`vbenjs/vben-admin-monorepo`) and the role this package plays
> in a real vben app. **Replace this file with real content when (and
> only when) the corresponding `packages/composables/`
> directory lands upstream.**

Do **not** implement against this placeholder — code that imports from
`@vben/composables` will fail to typecheck.
## When this package has Vue components

Most `@vben/composables` modules are **SFCs** (`.vue` with `<script setup lang="ts">`).
Follow the conventions below.

## Component file shape

```vue
<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@vben/utils';

interface Props {
  title: string;
  size?: 'small' | 'default' | 'large';
  disabled?: boolean;
}
const props = withDefaults(defineProps<Props>(), {
  size: 'default',
  disabled: false,
});
const cls = computed(() => cn('vben-x', `vben-x--${props.size}`));
</script>

<template>
  <div :class="cls" :aria-disabled="disabled || undefined">
    <slot>{ title }</slot>
  </div>
</template>
```

## Conventions

- **`<script setup lang="ts">`** is mandatory; no Options API.
- **Single root** allowed only when wrapper styles are pure; otherwise
  use `Fragment` or wrap with a meaningful element.
- **`defineOptions({ name: 'XxxYyy' })`** for `keep-alive` friendly names.
- **`v-model`** via `defineModel<T>('value')` (Vue 3.4+) or explicit
  `defineProps` + `defineEmits`.
- **Props with defaults** — always use `withDefaults(defineProps<…>(), {})`,
  not runtime object form.
- **Style** — `<style scoped>` only for component-local tweaks; layout
  primitives must remain styleless and consume `useAppTheme` tokens.

## Naming rules

| Thing | Rule | Example |
|---|---|---|
| File | `PascalCase.vue` | `VbenModal.vue` |
| Component name | `PascalCase` (no `Vben-` kebab unless global) | `VbenModal` |
| Directory | `kebab-case/` | `vben-modal/` |
| Slot | camelCase | `header`, `footer`, `trigger` |
| Event | `update:*` for v-model, otherwise `kebab-case` | `update:open`, `close` |

## Code example (real-style, 12+ lines)

```vue
<script setup lang="ts">
import { ref, watch } from 'vue';
import { VbenButton } from '@vben/composables/components';
import { useAppTheme } from '@vben/hooks';

interface Props {
  open: boolean;
  title?: string;
  onConfirm?: () => Promise<void> | void;
}
const props = defineProps<Props>();
const emit = defineEmits<{ (e: 'update:open', v: boolean): void }>();
const loading = ref(false);
const theme = useAppTheme();
async function handleConfirm() {
  if (!props.onConfirm) return emit('update:open', false);
  loading.value = true;
  try { await props.onConfirm(); }
  finally { loading.value = false; emit('update:open', false); }
}
watch(() => props.open, (v) => {
  if (!v) loading.value = false;
});
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="vben-x" :data-theme="theme.mode">
      <h3>{ title }</h3>
      <VbenButton :loading="loading" @click="handleConfirm">OK</VbenButton>
    </div>
  </Teleport>
</template>
```

## Forbidden

- ❌ No Options API (`export default { ... }`) — only `<script setup>`.
- ❌ No `any` in prop types — declare interfaces.
- ❌ No `defineProps` without `withDefaults` when defaults exist.
- ❌ No inline `<style>` colors — use `useAppTheme()` tokens.
- ❌ No mixing kebab-case and PascalCase in one component's name space.
- ❌ No importing UI from another component library directly — go through
  `@vben/composables`.
