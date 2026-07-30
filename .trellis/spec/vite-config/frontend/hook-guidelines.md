# @vben/vite-config Hooks — Vite Plugin Lifecycle

> "Hooks" here = Vite plugin hooks (`name`, `config`, `configResolved`,
> `transform`, `generateBundle`, `writeBundle`, `closeBundle`). Each plugin is
> a function returning a `PluginOption[]`. Source verified against
> `internal/vite-config/src/plugins/` v5.7.0.

## 模式: Plugin = 函数, 返回 PluginOption[]

每个 plugin 是 named async function,返回数组(支持多个 vite hook):

```ts
// src/plugins/print.ts (verified 模式)
import type { PluginOption } from 'vite';

async function vitePrintPlugin(options?: PrintPluginOptions): Promise<PluginOption[]> {
  const { infoMap = {} } = options ?? {};
  const pkg = await readPackageJSON(process.cwd());
  const meta = {
    name: pkg?.name,
    version: pkg?.version,
    ...infoMap,
  };

  const printPlugin: PluginOption = {
    name: 'vben:print',
    apply: 'build',
    enforce: 'post',
    closeBundle() {
      console.log('\n');
      const labels = Object.keys(meta);
      const maxLabelLen = Math.max(...labels.map((l) => l.length));
      const printData = labels.reduce<string[]>((acc, key) => {
        const value = (meta as any)[key];
        acc.push(`${key.padEnd(maxLabelLen)}: ${value ?? '-'}`);
        return acc;
      }, []);
      console.log(printData.join('\n'));
    },
  };

  return [printPlugin];
}
```

## Conditional Plugin Loader

`src/plugins/index.ts` 集中调度(verified):

```ts
async function loadConditionPlugins(conditionPlugins: ConditionPlugin[]) {
  const plugins: PluginOption[] = [];
  for (const conditionPlugin of conditionPlugins) {
    if (conditionPlugin.condition) {
      const realPlugins = await conditionPlugin.plugins();
      plugins.push(...realPlugins);
    }
  }
  return plugins.flat();
}
```

`ConditionPlugin` (from `typing.ts`):

```ts
interface ConditionPlugin {
  /** boolean — true 时加载 */
  condition?: boolean;
  plugins: () => PluginOption[] | PromiseLike<PluginOption[]>;
}
```

## Common Hooks (用法)

| Vite Hook           | 谁用 (verified)                          | 作用               |
| ------------------- | ---------------------------------------- | ------------------ |
| `transformIndexHtml` | `viteHtmlPlugin`                         | inject app config  |
| `transform`         | `viteDayjsPlugin`                        | 替换 dayjs 引入    |
| `config`            | `viteVxeTableImportsPlugin`              | alias rewrite      |
| `configResolved`    | `viteTailwindReferencePlugin`            | tailwind context   |
| `closeBundle`       | `vitePrintPlugin`, `viteArchiverPlugin`  | build 收尾         |
| `generateBundle`    | `viteImportMapPlugin`, `viteMetadataPlugin` | artifacts       |
| `writeBundle`       | `viteLicensePlugin`                      | banner 注入        |

## Conventions

- **Name convention**:`vben:{plugin-name}` (`vben:print`, `vben:html`, `vben:license`)
- **返回数组** —— 即便只有一个 plugin,也返回 `[plugin]`
- **`apply: 'build' | 'serve'`** —— 必须显式(默认 both,但 print 只 build)
- **`enforce: 'pre' | 'post'`** —— 替代 `transformIndexHtml: 'pre'`,更安全
- **async 插件** —— 可以用 `await readPackageJSON()` 在 plugin 函数顶部

## Naming

- 文件:`src/plugins/{name}.ts`,`{name}` 全小写,kebab(`extra-app-config.ts`)
- export:`vite{Name}Plugin` (camelCase from kebab) → `viteExtraAppConfigPlugin`
- plugin name:`vben:{kebab-name}` (`vben:inject-app-loading`)

## 修改 plugin 时的 check list

```text
1. update src/plugins/{name}.ts
2. (若新增)export from src/plugins/index.ts
3. 若 option shape 变,update src/typing.ts 的 XxxPluginOptions
4. 检查 src/config/application.ts / library.ts 是否需要传默认值
5. write snippet doc 到对应 .trellis/spec/vite-config/frontend/{file}
```

## Forbidden

- ❌ 不要在 plugin 里 mutate `vite: UserConfig` 外部引用 —— 副作用会传染
- ❌ 不要把 `name: 'vben:print'` 改成 `'print'` —— 同名冲突会引发 plugin 静默覆盖
- ❌ 不要让 `viteHtmlPlugin` 默认打开(用户可能想用 vite default HTML)
- ❌ 不要在 plugin 用 `console.log` 替代 `vitePrintPlugin` —— 已经统一管理
- ❌ 不要写 `enforce: 'pre'` 时的 plugin 名字 冲突(`unplugin-vue-components` 等)
- ❌ 不要把 `process.cwd()` 之外的 cwd 传给 `readPackageJSON` —— 给 library 时它跨 workspace
