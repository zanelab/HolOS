# @vben/node-utils Directory Structure

> 真实布局 for `internal/node-utils/` (the workspace package `@vben/node-utils`).

## 目录树（2026-07-29 核对）

```
internal/node-utils/
├── package.json                # name "@vben/node-utils" v5.7.0
├── scripts/
│   └── stub.mjs               # stub dist (no real build needed; downstream packages use tsx)
├── tsconfig.json
└── src/
    ├── index.ts               # public API barrel — re-exports helpers
    ├── constants.ts           # error/priority constants
    ├── date.ts                # date formatting helpers
    ├── formatter.ts           # bytes / duration formatters
    ├── fs.ts                  # mkdirp, atomic-write, file-replace helpers
    ├── git.ts                 # git command wrappers (used by Trellis scripts)
    ├── hash.ts                # sha-256 + content-hash helpers
    ├── monorepo.ts            # workspace package detection (find apps / packages / internal)
    ├── path.ts                # path join / relative / posix helpers
    ├── spinner.ts             # stdout-based progress (no TTY dependency)
    └── __tests__/             # unit tests for each module
        ├── fs.test.ts
        ├── hash.test.ts
        └── ...
```

## 约定

- 仅 **纯函数 helpers**。无 I/O 类，无全局状态。
- **Single barrel** at `src/index.ts`. Don't deep-import (`@vben/node-utils/internals/...`) from caller code.
- **友好树摊**：单独 export 每个函数；不要暴露一个包含全部内容的对象。
- **Tests live alongside source** in `__tests__/` (Vitest convention).
- **`stub.mjs`** in `scripts/` provides a fake `dist/index.mjs` so downstream consumers (run via `tsx`) don't need a real build step.

## 禁止

- ❌ Don't add CLI code here — that's `@vben/vsh`.
- ❌ Don't add platform-specific code (Node-only) outside `node:` imports — keep imports portable.
- ❌ Don't bundle external HTTP/network libraries — prefer Node built-ins.
- ❌ Don't ship `.env` reads from 本包 — that's an app concern.
