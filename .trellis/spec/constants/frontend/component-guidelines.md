# @vben/constants "Component" Style - Constants / Types

## 模式: explicit named exports

```ts
export const LOGIN_PATH = '/auth/login';
export type LayoutType = "sidebar-nav" | "mixed-nav" | /* ... */
export interface UserInfo {
  id: string;
  realName: string;
}
```

## 用法

```ts
import { LOGIN_PATH, type UserInfo, type LayoutType } from '@vben/constants';
```

## 禁止

- Don't add IO functions
- Don't add Vue refs
- Don't bundle into namespaced objects
