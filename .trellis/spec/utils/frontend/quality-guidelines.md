# @vben/utils Quality Guidelines

> Strict-mode TS, 4-space, single quotes.

## Tests

Co-located tests: __tests__/<name>.test.ts

```bash
pnpm --filter @vben/utils test
```

## Forbidden

- Don't introduce dependencies
- Don't add side-effect imports
