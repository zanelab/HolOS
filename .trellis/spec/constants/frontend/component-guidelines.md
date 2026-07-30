# @vben/constants "Component" Style — Constants & Types

> No Vue components. "Components" are typed const values and types.

## Pattern: 独立命名导出

```ts
// 来自 packages/constants/src/core.ts 风格
export const LOGIN_PATH = '/auth/login';
export const HOME_PATH = '/dashboard';

export type LayoutType =
  | 'full-content'
  | 'header-mixed-nav'
  | 'header-nav'
  | 'header-sidebar-nav'
  | 'mixed-nav'
  | 'sidebar-mixed-nav'
  | 'sidebar-nav';

export interface UserInfo {
  id: string;
  realName: string;
  email?: string;
  avatar?: string;
  homePath: string;
}
```

## Usage from apps

```ts
// 应用代码通常从 @vben/constants 拉 const + type
import {
  LOGIN_PATH,
  HOME_PATH,
  type LayoutType,
  type UserInfo,
} from '@vben/constants';

// 在 router/guard.ts 用
if (to.path === LOGIN_PATH) { ... }

// 在 preferences store 用
preferences.app.layout = 'mixed-nav' satisfies LayoutType;
```

## Tree-shaking 验证

`@vben/constants` 包应该这样使用:
```ts
// ✅ Good — 只 import 用到的,rollup tree-shake 其他
import { LOGIN_PATH } from '@vben/constants';
```

而不是:
```ts
// ❌ Bad — 全部引入
import * as C from '@vben/constants';
```

## 如何添加新常量

1. 在 `src/core.ts` (或新文件) 添加 const / type
2. **不要** 加 JSDoc-only 的常量,每个 const 应该有真实使用场景
3. **同时** 更新 `src/index.ts` 的 re-export
4. (可选) Bump 版本,4-digit semver: PATCH 增加

## Forbidden

- ❌ **不要** 添加非 const 的 helper function(用 `@vben/utils`)
- ❌ **不要** 在 this 包添加 `useXxx` Vue hooks
- ❌ **不要** 在 this 包 mutate 值(`Object.freeze` 也不可以 — const 已天然不可变)
- ❌ **不要** 引入运行时依赖(`@vben/utils` 引用是 @vben-internal 允许,但不要引入 lodash 等)
