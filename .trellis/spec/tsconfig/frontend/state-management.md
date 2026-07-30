# @vben/tsconfig: Stateless by Design

> Configs are static. There is no state, no Pinia, no Redux, no `ref()`, no
> singleton. `internal/tsconfig/` (verified v5.7.0) ships **5 immutable JSON
> files** that the TypeScript compiler merges at parse-time.

## 唯一 "state-like" 概念:extends chain

`tsconfig.json` 的 `state` 实际上是 `extends` 链:

```
apps/web-holos/tsconfig.json
   ↓ extends
@vben/tsconfig/web-app.json     ← this package
   ↓ extends
@vben/tsconfig/web.json
   ↓ extends
@vben/tsconfig/base.json        ← strict baseline
```

每一层只 *添加/覆盖* 字段,从不 *修改* 父级。这意味着:

- 子 config 完全 deterministic given 父 config
- 没有 initialization order 问题
- 没有 race conditions,无需 store

## 模式: 静态、不变、可在 compile-time 求值

`base.json` (verified v5.7.0) 显式:

```jsonc
{
  "compilerOptions": {
    "noEmit": true,
    "removeComments": true,
    "sourceMap": false,
    "isolatedModules": true
  }
}
```

—— 全部属性都是 `compile-time`,不进入运行时,自然 `immutable`。

## Conventions

- **JSON 必须 immutable** —— 一旦发布,版本升 `5.x → 5.x+1` 才变
- **不要 mutate `compilerOptions`** via lodash.merge 之类 —— IDE 会读到错误值
- **不要动态生成 JSON** —— 不能 `JSON.stringify(baseConfig, computedAt)`
- **不要 import `@vben/constants` 到 variant** —— variant 是数据,不是代码
- **不要 catch all `extends`** —— 只 extends 本包内其他 variant 或 `./base.json`

## 字段求值顺序 (effective merge)

```
1. extends 链 → base
2. compilerOptions (deep merge, child wins)
3. files / include / exclude (child full replaces parent)
4. references (concatenated)
5. $schema / display (child full replaces parent)
```

## Naming

- variable-style overrides 名写在 `compilerOptions` 内,标准 ts 字段名
- 例外:`display` 是 vben 私有字段,IDE 会读取
- 顶层字段顺序:`$schema` → `display` → `extends` → `compilerOptions` → `exclude`/`include`

## Forbidden

- ❌ 不要把 `compilerOptions.noEmit` 改成 `false` —— base.json 永远 noEmit
- ❌ 不要在 variant 里加 `compilerOptions.paths` —— paths 应在 app 自己的 tsconfig
- ❌ 不要 mutating 这个包内部的对象在 CI/build process
- ❌ 不要引入 runtime state 管理 (Pinia/Redux/Zustand) 到 tsconfig 包
- ❌ 不要把 `.jsonc` 写到 tsconfig variant —— strict JSON only
- ❌ 不要加 `compileOnSave` —— 这是 IDE-only,本包不该建议
