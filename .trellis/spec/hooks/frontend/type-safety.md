# hooks Type Safety

> **PLACEHOLDER DOCS** - This package does not exist in the workspace at this time. Expected conventions are based on vben v5.7.0 monorepo. Replace these files with real content when the package is added.

## Expected Config

- Apps: tsconfig.json extends @vben/tsconfig/web-app.json
- Libs: tsconfig.json extends @vben/tsconfig/library.json
- Strict mode ON (no implicit any, strict null checks)

## Expected Patterns

```ts
import type { RouteRecordRaw } from "vue-router";
const routes: RouteRecordRaw[] = [...];

// Composables types
interface Props { title: string; count?: number; }
const props = withDefaults(defineProps<Props>(), { count: 0 });

// API responses
export interface XResponse { id: string; }
```

## Forbidden

- Do not use any
- Do not disable strict mode per-file
- Do not use as cast to silence errors
- Do not implement against this phantom package
