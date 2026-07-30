# @vben/utils Quality Guidelines

> 严格模式 TS, 4-space, single quotes.

## 测试s

Co-located tests: __tests__/<name>.test.ts

```bash
pnpm --filter @vben/utils test
```

## 禁止

- Don't introduce dependencies
- 不要添加带副作用的 import
