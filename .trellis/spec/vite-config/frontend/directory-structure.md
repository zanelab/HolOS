# @vben/vite-config Directory Structure

> Verified `internal/vite-config/src/` (v5.7.0). This package builds with
> `tsdown` and ships `dist/index.{mjs,d.ts}`. Consumed by apps and packages
> via workspace alias `@vben/vite-config`.

## 目录树 (verified)

```
@vben/vite-config/                    # workspace: internal/vite-config/
├── package.json                      # name "@vben/vite-config"
├── tsconfig.json
├── tsdown.config.ts                  # 库构建配置 (ESM)
├── dist/
│   ├── index.mjs                     # tsdown 输出 — 单 file
│   ├── index.d.ts                    # 单 .d.ts,所有类型 re-export
│   └── default-loading-antd.html
└── src/
    ├── index.ts                      # 5 行 barrel — re-exports config, options, plugins, typing, env
    ├── options.ts                    # defaultImportmapOptions, getDefaultPwaOptions
    ├── typing.ts                     # 所有 plugin options 接口
    ├── config/
    │   ├── index.ts                  # 智能 detection (web vs library)
    │   ├── application.ts            # defineApplicationConfig (apps)
    │   ├── library.ts                # defineLibraryConfig (packages)
    │   └── common.ts                 # getCommonConfig (build defaults)
    ├── plugins/
    │   ├── index.ts                  # loadApplicationPlugins / loadLibraryPlugins
    │   ├── archiver.ts               # zip 归档
    │   ├── dayjs.ts                  # dayjs locale treeshake
    │   ├── extra-app-config.ts       # inject 配置文件
    │   ├── html.ts                   # html transform + minify
    │   ├── importmap.ts              # esm.sh/jspm.io CDN
    │   ├── inject-app-loading/       # 启动动画 HTML
    │   ├── inject-metadata.ts        # build metadata
    │   ├── license.ts                # banner
    │   ├── nitro-mock.ts             # dev mock server
    │   ├── print.ts                  # 控制台 print build info
    │   ├── tailwind-reference.ts     # tailwind vite plugin
    │   └── vxe-table.ts              # vxe-table 全局注册
    └── utils/
        └── env.ts                    # loadAndConvertEnv, loadEnv
```

## 依赖关系 (verified)

```ts
// 从 src/index.ts (5 行)
export * from './config';
export * from './options';
export * from './plugins';
export type * from './typing';
export { loadAndConvertEnv } from './utils/env';
```

App-side 消费:

```ts
// apps/web-holos/vite.config.ts
import { defineConfig } from '@vben/vite-config';

export default defineConfig(async () => {
  return { application: { compress: false } };
});
```

## Patterns

- **5 行 barrel** —— `src/index.ts` 仅作 re-export,无逻辑
- **每个 plugin 一个 .ts** —— `src/plugins/{name}.ts`,且 named export 函
  数式插件(`viteXxxPlugin(options)`)
- **conditional plugins** —— 集中于 `src/plugins/index.ts`,统一 `loadXxxPlugins`
- **`loadAndConvertEnv`** —— 唯一允许 read .env.* file 的入口

## Conventions

- **单 `index.ts` 暴露所有 API** —— 没有 `/config`、`/plugins`、`/typing` 子 barrel
- **`src/utils/` 不是公开入口** —— `loadAndConvertEnv` 通过顶层 `export { loadAndConvertEnv }` 单独导
- **`dist/` 由 tsdown 产出** —— 永远手编,源码全在 `src/`
- **`tsconfig` 在包根** —— 内部包也用 tsconfig.json(extends `@vben/tsconfig/base`)

## Naming

- 文件名 camelCase 或 kebab-case:plugin 用 kebab(`extra-app-config.ts`),其
  余 camelCase
- 函数导出 `defineXxxConfig`,`viteXxxPlugin`,`loadXxxPlugins`,`getXxxConfig`
- 类型导出 `XxxOptions` 后缀(plugin options)或 `XxxConfig`(config return)

## Forbidden

- ❌ 不要在 `src/` 顶层加 `index.ts` 之外的入口文件(`main.ts`、`app.ts` 等)
- ❌ 不要将 `loadAndConvertEnv` 之外的 util 暴露到顶层
- ❌ 不要把 ENV 解析逻辑分散到 `config/application.ts` —— 已在 `utils/env.ts` 集中
- ❌ 不要在 plugin 文件里 hardcode import `'./index'` —— 循环依赖
- ❌ 不要新建 `dist/` 内容手编(永远走 `tsdown`)
- ❌ 不要把 `package.json` 的 `version` 与内部 dist 不一致 —— publish 前 sync
