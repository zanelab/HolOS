# @vben/utils Component Guidelines

> No Vue components. Functions only.

## Pattern: explicit named exports

```ts
export function mergeRouteModules(modules: RouteModule[]): RouteRecordRaw[] {
  // implementation
}
```

## Usage

```ts
import { mergeRouteModules } from '@vben/utils';
const routes = mergeRouteModules([dashboardModule, demosModule]);
```

## Forbidden

- Don't bundle into classes / namespaces
- Don't add side effects
- Don't return generic any
