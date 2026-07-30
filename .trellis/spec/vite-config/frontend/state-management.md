# @vben/vite-config State Management — Implicit via Plugin Options

> This package does **not** export `ref()` / `reactive()` / Pinia stores.
> "State" here is plugin options merged at definition time and held in
> closure scope. Source verified against `internal/vite-config/src/`
> v5.7.0.

## 唯一的 "state" 概念:Plugin Options

`ApplicationPluginOptions` is a mega-config object — passed to
`loadApplicationPlugins()` and destructured per-flag:

```ts
// src/typing.ts (verified, abridged)
interface CommonPluginOptions {
  devtools?: boolean;
  env?: Record<string, any>;
  injectMetadata?: boolean;
  isBuild?: boolean;
  mode?: string;
  visualizer?: boolean | PluginVisualizerOptions;
}

interface ApplicationPluginOptions extends CommonPluginOptions {
  archiver?: boolean;
  archiverPluginOptions?: ArchiverPluginOptions;
  compress?: boolean;
  compressTypes?: ('brotli' | 'gzip')[];
  dayjs?: boolean;
  extraAppConfig?: boolean;
  html?: boolean | HtmlPluginOptions;
  i18n?: boolean;
  importmap?: boolean;
  importmapOptions?: ImportmapPluginOptions;
  injectAppLoading?: boolean;
  injectGlobalScss?: boolean;
  license?: boolean;
  nitroMock?: boolean;
  nitroMockOptions?: NitroMockPluginOptions;
  print?: boolean;
  printInfoMap?: PrintPluginOptions['infoMap'];
  pwa?: boolean;
  pwaOptions?: Partial<PwaPluginOptions>;
  vxeTableLazyImport?: boolean;
}
```

## 状态如何在内部流动

```
┌──────────────────────────┐
│ apps/web-holos/.env      │   ← filesystem state
└──────────┬───────────────┘
           ▼ (loadAndConvertEnv)
┌──────────────────────────┐
│ Partial<ApplicationOp…>  │   ← in-memory state
└──────────┬───────────────┘
           ▼ (...envConfig, ...application spread)
┌──────────────────────────┐
│ loadApplicationPlugins() │   ← merges & dispatches
└──────────┬───────────────┘
           ▼ loadConditionPlugins([...])
┌──────────────────────────┐
│ PluginOption[] (frozen)  │   ← Vite holds reference
└──────────────────────────┘
```

## Conventions

- **No mutability** —— options 是 plain object,但 spread 后 readonly
- **Spread order matters** —— `...envConfig, ...application` 在
  `application.ts` line 53,让 application 覆盖 ENV
- **No Redux/Zustand** —— 这个包不该 be reactive
- **Plugin flags 是 boolean | options** —— 不是 always `{ enabled: true }`

## 修改 state shape 的工作流

```text
1. update src/typing.ts
2. update src/config/application.ts (默认值, ENV 转译)
3. update src/plugins/index.ts (条件加载)
4. (若 ENV flag)update src/utils/env.ts (loadAndConvertEnv 解构)
5. (若 default PWA/importmap)update src/options.ts
6. write .trellis/spec/vite-config/frontend/{file} 文档
```

## Naming

- Options: `XxxPluginOptions` (在 typing.ts 集中)
- 默认值函数名: `getDefaultXxx(...)` (`getDefaultPwaOptions(appTitle)`)
- default 常量: `defaultXxx` (`defaultImportmapOptions`)

## Forbidden

- ❌ 不要在 vite-config 里引入 `pinia`、`vuex`、redux 等
- ❌ 不要把 plugin flags 设计为 nested namespace(`devtools.enabled` 而
  非 `devtools:boolean`)—— 顶层 flag 一律 flatten
- ❌ 不要让 ENV 之外的来源(URL query, cookie)参与 plugin state
- ❌ 不要让 plugin options 是 class —— 保持 plain object 序列化能力
- ❌ 不要在 `options.ts` 加 mutable default (`Object.freeze` 也不行,vite 会读)
- ❌ 不要在 `plugin` 内调用 `defineXxxConfig` 嵌套 —— 这是 config 层 API
