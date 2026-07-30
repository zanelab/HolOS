# @vben/types "Component" Style - Constants / Types

## 模式：显式命名导出

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
import { LOGIN_PATH, type UserInfo, type LayoutType } from '@vben/types';
```

## 禁止

- Don't add IO functions
- 不要添加 Vue refs
- 不要打包到命名空间对象中
