# @vben/icons Type Safety

> Vue SFC + IconifyIcon props typed.

```ts
import type { PropType } from 'vue';
export default defineComponent({
  props: {
    icon: { type: String as PropType<string>, required: true },
    size: { type: Number, default: 16 },
  },
});
```
