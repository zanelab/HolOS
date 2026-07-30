# @vben/constants Type Safety

> 严格模式 TS. Zero runtime concerns.

```ts
export type AccessToken = null | string;
export const LAYOUTS = ['sidebar-nav', 'mixed-nav'] as const;
```

## 禁止

- 不要使用 any
- 不要使用 Object 作为类型
