# @vben/oxlint-config Directory Structure

> Config-only package consumed via workspace alias.

## Tree (verified)

```
@vben/oxlint-config/
├── package.json                # workspace name "@vben/oxlint-config"
├── tsconfig.json
└── src/
    ├── index.ts                # re-exports everything
    └── (one or more config files)
```

## Conventions

- **Config objects** exported as named const
- **Single barrel** at src/index.ts
- **No real build step** - consumed via tsx
- **scripts/stub.mjs** provides fake dist/index.mjs

## Forbidden

- Don't add runtime code (HTTP, file IO, async)
- Don't add CLI
- Don't add tests
