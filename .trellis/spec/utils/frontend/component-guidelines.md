# @vben/utils Component Guidelines

> 无 Vue 组件。 Functions only.

## 模式: explicit named exports

```ts
export function mergeRouteModules(modules: RouteModule[]): RouteRecordRaw[] {
  // implementation
}
```

## 用法

```ts
import { mergeRouteModules } from '@vben/utils';
const routes = mergeRouteModules([dashboardModule, demosModule]);
```

## 禁止

- Don't bundle into classes / namespaces
- Don't add side effects
- Don't return generic any
