# @vben/preferences Type Safety

> Strict-mode TS. Zero runtime concerns.

```ts
export type AccessToken = null | string;
export const LAYOUTS = ['sidebar-nav', 'mixed-nav'] as const;
```

## Forbidden

- Don't use any
- Don't use Object as a type
