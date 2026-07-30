# @vben/tsconfig: Hooks Not Applicable

> Configuration package `internal/tsconfig/` ships only JSON. There are no
> Vue composables, no React hooks, no lifecycle functions — and there should
> not be any. Source verified against v5.7.0 (5 JSON variants, no `.ts`/`.js`).

## 为什么 "hooks" 不适用

tsconfig 是 **静态声明性数据** —— 编译器在解析时读取,运行时从不触发。
它没有 React/Vue 那种 "use client" / response-driven lifecycle 的概念。

如果在 apps 里需要运行时行为,对应的位置是:

| 需求              | 落在哪里                  |
| ----------------- | ------------------------- |
| FS、进程、子进程   | `apps/*/build/script.ts`  |
| 运行时 SVG 处理   | `packages/icons`          |
| ENV 解析          | `@vben/node-utils/env`   |
| Vue composable    | `packages/composables/`   |
| Pinia store       | `packages/stores/`        |

## 错误示例(曾在 review 中阻挡)

```ts
// ❌ Bad — 在 tsconfig 包里写逻辑(实际从未发生,仅作示例)
// /internal/tsconfig/src/hooks/useCompiler.ts
export function useCompiler() {
  const root = process.cwd();
  return readFileSync(join(root, 'tsconfig.json'));
}
```

正解:把文件 IO 放在 `@vben/node-utils`,这里只导出 JSON。

## 唯一 "service-like" 模式

`loadAndConvertEnv` 的等价物在 vite-config 中实现 —— **不在 tsconfig**:

```ts
// /internal/vite-config/src/utils/env.ts (实际 verify)
export async function loadAndConvertEnv() {
  const env = loadEnv(mode, process.cwd());
  return convertViteEnv(env);
}
```

tsconfig 永远不引入 `node:fs` 或 `node:process`。

## Conventions

- **0 个 `.ts` 文件** —— `find internal/tsconfig -name "*.ts"` 应返回空
- **0 个运行时 import** —— 不需要 `import type { RuleSet } ...`
- **0 个 `dist/`** —— JSON 直接 `extends`,不编译
- **0 个测试** —— TS 编译器的官方测试覆盖继承行为
- **`package.json` 不需要 `main`、`module`** —— 消费者只引用 `.json`

## Forbidden

- ❌ 不要在 tsconfig 包加 `useXxx` Vue/React hook
- ❌ 不要加 `process.env` / `fs.readFile` 之类的运行时逻辑
- ❌ 不要为这个包加 Vitest/Jest config —— 它不该被运行时执行
- ❌ 不要为这个包加 `tsconfig.json` —— 会干扰 IDE 解析链
- ❌ 不要写 CLI 工具(比如 `pnpm tsconfig-tools`)在这个包
- ❌ 不要在 variant 中混用 verbatimModuleSyntax 与 `export = `
