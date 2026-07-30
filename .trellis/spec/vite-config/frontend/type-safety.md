# @vben/vite-config Type Safety

> Type-safety is anchored by `src/typing.ts` — every plugin option interface
> lives there. Strict TS (extends `@vben/tsconfig/base.json`) means
> `verbatimModuleSyntax`, `noUncheckedIndexedAccess`, etc. Source verified v5.7.0.

## 核心原则:options 是 typed contract

每一个 plugin flag 都对应一个 typed interface。修改一个 flag 必须同时:

1. update `src/typing.ts` 的 `XxxPluginOptions`
2. update `src/config/application.ts` 的默认值
3. update `src/utils/env.ts` 解构(如 ENV flag)
4. 重生成 `dist/index.d.ts`(tsdown 在 build 自动)

## 关键 type 示例 (verified)

`PrintPluginOptions`:

```ts
interface PrintPluginOptions {
  /**
   * 打印的数据映射
   * @description 键值对形式的数据,将在控制台打印
   * @example
   * ```typescript
   * {
   *   'App Version': '1.0.0',
   *   'Build Time': '2024-01-01'
   * }
   * ```
   */
  infoMap?: Record<string, string | undefined>;
}
```

`NitroMockPluginOptions`:

```ts
interface NitroMockPluginOptions {
  /** Mock 服务器包名 @default '@vbenjs/nitro-mock' */
  mockServerPackage?: string;
  /** Mock 服务端口 @default 3000 */
  port?: number;
  /** 是否打印 Mock 日志 @default false */
  verbose?: boolean;
}
```

`ImportmapPluginOptions`:

```ts
interface ImportmapPluginOptions {
  /** CDN 供应商 @default 'jspm.io' */
  defaultProvider?: 'esm.sh' | 'jspm.io';
  /** ImportMap 配置数组 */
  importmap?: Array<{ name: string; range?: string }>;
  /** 手动配置 ImportMap */
  inputMap?: IImportMap;
}
```

`ApplicationPluginOptions`:

```ts
interface ApplicationPluginOptions extends CommonPluginOptions {
  archiver?: boolean;
  archiverPluginOptions?: ArchiverPluginOptions;
  compress?: boolean;
  compressTypes?: ('brotli' | 'gzip')[];
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

## Conventions

- **`XxxPluginOptions` interface 集中于 `src/typing.ts`** —— 不要分散到 plugin 文件
- **`type * from './typing'`** —— `src/index.ts` 用 type-only re-export
- **boolean flag = `boolean | options`** —— 而非 `{ enabled: true, options: {} }`
- **defaults 来自 `options.ts`** —— 而不是 typing.ts(separator of concerns)
- **`Record<string, string | undefined>`** 而不是 `any`(在 `infoMap` 体现)
- **`'brotli' | 'gzip'` 字面量 union** —— `compressTypes` 用 literal 限制

## Naming

- 接口 `XxxPluginOptions` 或 `XxxConfig`(如 `ApplicationPluginOptions`)
- type alias `Xxx`(如 `IImportMap`, `HtmlPluginOptions`)
- 文件内同类放在一个 namespace-like 接口里,不分散

## 修改 option 时的 contract

```text
[ ] interface 加字段(必填?optional?default?)
[ ] default 写在 src/options.ts 函数返回
[ ] ENV flag 加在 src/utils/env.ts 解构
[ ] dist 更新(tsdown 自动)
[ ] .trellis 文档同步
[ ] apps 端 typecheck 必须通过
```

## Forbidden

- ❌ 不要在 typing.ts 用 `any` —— 用 `Record<string, string | undefined>` 或 unknown
- ❌ 不要让 boolean flag 退化为 `{ enabled: true }` —— 保持 boolean literal
- ❌ 不要给已 union 的字段加第三种 type(如 `string | 'gzip' | 'brotli' | 'snappy'`)
- ❌ 不要让 plugin options 是 class —— 用 plain interface
- ❌ 不要把 `infoMap` 写成 `Record<string, any>` —— 已有 typed
- ❌ 不要遗漏 `import type` 用法 —— `verbatimModuleSyntax` 强制分离 type/value
