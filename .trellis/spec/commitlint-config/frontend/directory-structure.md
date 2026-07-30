# @vben/commitlint-config Directory Structure

> Config-only package consumed via workspace alias.

## 目录树 (verified)

```
@vben/commitlint-config/
├── package.json                # workspace name "@vben/commitlint-config"
├── tsconfig.json
└── src/
    ├── index.ts                # re-exports everything
    └── (one or more config files)
```

## 约定

- **Config objects** exported as named const
- **Single barrel** at src/index.ts
- **No real build step** - consumed via tsx
- **scripts/stub.mjs** provides fake dist/index.mjs

## 禁止

- Don't add runtime code (HTTP, file IO, async)
- Don't add CLI
- Don't add tests
