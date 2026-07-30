# @vben/icons Type Safety

> Vue SFC + IconifyIcon props typed via Vue 3 defineProps.

## SVG 文件 Types

多数 SVG files 0-arg 不需 script。但 `<IconifyIcon>` 需要:

```vue
<script setup lang="ts">
import type { PropType } from 'vue';

export default defineComponent({
  props: {
    icon: { type: String, required: true },
    size: { type: Number, default: 16 },
  },
});
</script>
```

## TS config

`packages/icons/tsconfig.json`:

```json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` enabled.

## Type Patterns

### 1. Strings (iconify icon name)

```ts
// 简单 — single string
defineProps<{ icon: string }>();

// const assertion for narrow string literal type
const ICON_NAME = 'lucide:home';
defineProps<{ icon: typeof ICON_NAME }>();
```

### 2. Numbers (size props)

```ts
defineProps<{
  size?: number;
}>();
```

### 3. Boolean props (e.g. disabled)

```ts
defineProps<{
  disabled?: boolean;
}>();
```

### 4. Combined

```ts
defineProps<{
  icon: string;
  size?: number;
  disabled?: boolean;
  spin?: boolean;
}>();
```

## Type Imports

Use `import type`:

```ts
import type { PropType } from 'vue';
```

Value imports have **no `type` prefix**:

```ts
import { defineComponent } from 'vue';
```

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/icons
```

## Strict Mode 验证

- `noUnusedLocals: true` — 不允许 unused imports
- `noUnusedParameters: true` — fn 参数必须用或前缀 `_`
- `verbatimModuleSyntax` — `import type` 显式标注

## Forbidden

- ❌ 不要用 `any` for icon name (用 `string` 或 specific literal type)
- ❌ 不要 disable strict mode in `tsconfig.json`
- ❌ 不要 `as` cast 来 silence errors — refactor
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 publish icons package 含 .d.ts generated to /dist (use side-effect-free src/index.ts)
