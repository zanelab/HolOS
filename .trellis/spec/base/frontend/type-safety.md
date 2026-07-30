# base Type Safety

> **PLACEHOLDER DOCS** - 本包 does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. 替换这些文件 real content when package 添加后.

## 预期配置

- Apps: tsconfig.json extends @vben/tsconfig/web-app.json
- Libs: tsconfig.json extends @vben/tsconfig/library.json
- 严格模式 ON (no implicit any, strict null checks)

## 预期模式

```ts
import type { RouteRecordRaw } from "vue-router";
const routes: RouteRecordRaw[] = [...];

// Composables types
interface Props { title: string; count?: number; }
const props = withDefaults(defineProps<Props>(), { count: 0 });

// API responses
export interface XResponse { id: string; }
```

## 禁止

- 不要 use any
- 不要在单个文件中关闭严格模式
- 不要使用 as 断言来压制类型错误
- 不要 implement against this phantom package
