# @vben/vite-config "Component" Style — Config Composables

> "Components" here = `defineConfig` / `defineApplicationConfig` /
> `defineLibraryConfig` / `defineXxxPlugin`. Source verified against
> `internal/vite-config/src/` v5.7.0.

## 核心 Component:`defineConfig`(自动 detect)

`src/config/index.ts` (verified) — 自动判断 application vs library:

```ts
import type { DefineConfig, VbenViteConfig } from '../typing';

import { existsSync } from 'node:fs';
import { join } from 'node:path';

import { defineApplicationConfig } from './application';
import { defineLibraryConfig } from './library';

export * from './application';
export * from './library';

function defineConfig(
  userConfigPromise?: DefineConfig,
  type: 'application' | 'auto' | 'library' = 'auto',
): VbenViteConfig {
  let projectType = type;

  // 根据包是否存在 index.html,自动判断类型
  if (projectType === 'auto') {
    const htmlPath = join(process.cwd(), 'index.html');
    projectType = existsSync(htmlPath) ? 'application' : 'library';
  }

  switch (projectType) {
    case 'application':
      return defineApplicationConfig(userConfigPromise);
    case 'library':
      return defineLibraryConfig(userConfigPromise);
    default:
      throw new Error(`Unsupported project type: ${projectType}`);
  }
}

export { defineConfig };
```

## "Application Component":`defineApplicationConfig`

```ts
// src/config/application.ts (verified, abridged)
function defineApplicationConfig(userConfigPromise?: DefineApplicationOptions) {
  return defineConfig(async (config) => {
    const options = await userConfigPromise?.(config);
    const { appTitle, base, port, ...envConfig } = await loadAndConvertEnv();
    const { command, mode } = config;
    const { application = {}, vite = {} } = options || {};
    const root = process.cwd();
    const isBuild = command === 'build';

    const plugins = await loadApplicationPlugins({
      archiver: true,
      compress: false,
      compressTypes: ['brotli', 'gzip'],
      devtools: true,
      env,
      extraAppConfig: true,
      html: true,
      i18n: true,
      importmapOptions: defaultImportmapOptions,
      // ...other plugin flags
      ...envConfig,
      ...application,
    });

    const applicationConfig: UserConfig = {
      base,
      build: { /* rolldownOptions */ },
      css: createCssOptions(injectGlobalScss),
      plugins,
      server: { host: true, port, warmup: { clientFiles: [...] } },
    };

    const mergedCommonConfig = mergeConfig(
      await getCommonConfig(),
      applicationConfig,
    );
    return mergeConfig(mergedCommonConfig, vite);
  });
}
```

## "Library Component":`defineLibraryConfig`

```ts
// src/config/library.ts (verified)
function defineLibraryConfig(userConfigPromise?: DefineLibraryOptions) {
  return defineConfig(async (config: ConfigEnv) => {
    const options = await userConfigPromise?.(config);
    const { command, mode } = config;
    const { library = {}, vite = {} } = options || {};
    const isBuild = command === 'build';

    const plugins = await loadLibraryPlugins({
      dts: false,
      injectMetadata: true,
      isBuild,
      mode,
      ...library,
    });

    const { dependencies = {}, peerDependencies = {} } =
      await readPackageJSON(root);

    const externalPackages = [
      ...Object.keys(dependencies),
      ...Object.keys(peerDependencies),
    ];

    const packageConfig: UserConfig = {
      build: {
        lib: {
          entry: 'src/index.ts',
          fileName: () => 'index.mjs',
          formats: ['es'],
        },
        rolldownOptions: {
          external: (id) =>
            externalPackages.some(
              (pkg) => id === pkg || id.startsWith(`${pkg}/`),
            ),
        },
      },
      plugins,
    };
    return mergeConfig(await getCommonConfig(), mergeConfig(packageConfig, vite));
  });
}
```

## Conventions

- **`defineConfig` 是用户入口** —— apps/packages 都用它,不要 import `defineApplicationConfig` / `defineLibraryConfig` 直接
- **`userConfig` 是 async function** —— 类型签名 `() => Promise<{ application?, vite? }>`
- **`loadAndConvertEnv()` 永远 in `defineApplicationConfig` 第一行** —— apps 必须 support ENV
- **library mode 自动 external 化 `dependencies` + `peerDependencies`** —— 不要手写 external
- **`getCommonConfig()` 提供 base build flags** —— `chunkSizeWarningLimit`, `sourcemap`

## Naming

- exported config fn: `define{Application|Library|Config}Config`
- exported plugin fn: `vite{Named}Plugin(options)` → `PluginOption[]`
- exported util fn: `load{Condition}Plugins`, `get{Default}Config`
- exported types: `ApplicationPluginOptions`, `LibraryPluginOptions`, `CommonPluginOptions`

## Forbidden

- ❌ 不要把 `defineConfig` 写成 sync —— 它**必须**支持 `await userConfigPromise()`
- ❌ 不要在 config 文件里 `process.cwd()` 之外 cwd 来源 —— 会破坏 monorepo
- ❌ 不要把 `defineApplicationConfig` 直接 export 在 `src/index.ts` 顶层(已 by `export * from './config'`)
- ❌ 不要省略 `await loadAndConvertEnv()` —— apps 默认就开
- ❌ 不要让 `library` build 不 externalize dependencies —— 包装后会爆 bundle
- ❌ 不要把 ENV 前缀从 `VITE_` 改了 —— apps 都依赖
