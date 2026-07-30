# @vben/styles Type Safety

> JS surface is tiny: `index.ts` + `style-exports.d.ts`.

## Purpose

`@vben/styles` exports a single string (the CSS asset) plus a re-exported
design module. Strict typing on the `.d.ts` ensures consumers can `import`
the stylesheet as a typed module.

## TS module declarations

```ts
// packages/styles/src/style-exports.d.ts
declare const stylesheet: string;
export default stylesheet;
```

This guarantees that any `import stylesheet from '@vben/styles/<flavor>'`
has the inferred type `string` — easy to wrap in `CSSStyleSheet` plugins.

## Public barrel

```ts
// packages/styles/src/index.ts (verified)
import '@vben-core/design';
```

The line is a **side-effect import** — it pulls in design tokens but
exposes no symbol. Consumers that want a typed handle get it via
`style-exports.d.ts`.

## Consuming typed import

```ts
// apps/web-antdv-next/src/bootstrap.ts
import '@vben/styles';
import '@vben/styles/antdv-next';
// No value to bind — pure side-effect imports.
```

```ts
// apps/web-antdv-next/src/adapter/component/index.ts (real)
import stylesheet from '@vben/styles/antdv-next';
// stylesheet: string
```

## TS config

```json
// packages/styles/tsconfig.json
{
  "extends": "@vben/tsconfig/library.json"
}
```

Strict mode + `verbatimModuleSyntax` + `noUnusedLocals`.

## Conventions

- **Single `declare` per asset** — never hand-type modules.
- **`@vben-core/design`** is the type source for design tokens; this
  package just re-exports.
- **No `any`** in any TS file.
- **No `as` casts** to silence type errors.
- **`verbatimModuleSyntax`** — `import type` for type-only imports.

## Typecheck

```bash
pnpm typecheck
pnpm typecheck --filter @vben/styles
```

## Forbidden

- ❌ 不要 use `any` for the stylesheet — `string` is the precise type
- ❌ 不要 `as` cast the stylesheet result — accept `string`
- ❌ 不要 disable `strict: true` in `tsconfig.json`
- ❌ 不要 use `@ts-ignore` without `// why:` comment
- ❌ 不要 remove `style-exports.d.ts` — module typing depends on it
- ❌ 不要 ship a `.d.ts` that exports `default: any` — defeats the type
- ❌ 不要 import `@vben/styles` from `@vben-core/design` — circular
- ❌ 不要 import a flavor stylesheet under a wrong path
   (e.g., `@vben/styles/anything-oops`)
