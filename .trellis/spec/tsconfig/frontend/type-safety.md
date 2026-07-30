# @vben/tsconfig Type Safety

> 严格模式 TS. tsconfig 包本身是 JSON,严格性体现在 *consumer code* 是否通过
> 编译。Source verified against `internal/tsconfig/{base,library,node,web,web-app}.json` v5.7.0.

## 核心原则

tsconfig 包发布的不是代码,而是 **type-safety 让 apps 强制遵循的约束**:

```jsonc
// base.json 强制项
{
  "compilerOptions": {
    "strict": true,                       // 顶级 strict 总开关
    "strictNullChecks": true,
    "noImplicitAny": true,
    "noImplicitOverride": true,           // 子类 override 必须显式标记
    "noImplicitThis": true,
    "noFallthroughCasesInSwitch": true,   // switch 必须显式 break/return
    "noUncheckedIndexedAccess": true,     // arr[i] 类型为 T | undefined
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "verbatimModuleSyntax": true,         // 强 type 与 value import 分离
    "isolatedModules": true               // 单文件也能编译,Vite/swc 必需
  }
}
```

## 各 variant 的 type 故事

### `library.json` —— 让库 typed

```jsonc
{
  "compilerOptions": {
    "declaration": true,     // 输出 .d.ts
    "noEmit": false          // 库包需要 emit .js + .d.ts
  }
}
```

### `web.json` —— web 包默认

```jsonc
{
  "compilerOptions": {
    "jsx": "preserve",
    "jsxImportSource": "vue",
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "moduleResolution": "bundler"
  }
}
```

### `node.json` —— Node-only 包

```jsonc
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "types": ["node"]
  }
}
```

### `web-app.json` —— 最终 app

```jsonc
{
  "extends": "./web.json",
  "compilerOptions": {
    "types": ["vite/client", "@vben/types/global"]
  }
}
```

## Conventions

- **type imports** —— 在 consumer 端必须用 `import type { X } from '...'`
  (因为 `verbatimModuleSyntax: true`)。`base.json` strict 模式已强制。
- **`@vben/types/global`** —— 全局 type augmentation 由 `web-app.json` 引入
- **不允许的 pragmas** —— 不要用 `@ts-ignore`,允许 `@ts-expect-error`
- **DOM types** —— 通过 `web.json` 的 `lib: ["DOM", "DOM.Iterable"]`
- **`strictNullChecks`** —— 必须显式处理 `undefined`,不可选字段用 `T | undefined`

## Naming

- `compilerOptions` 字段全部 camelCase (`strictNullChecks`)
- variant 文件名 kebab-case (`web-app.json`)
- 不要重新发明 `target`,`module`,`lib` —— extends 后 *不覆盖*

## 修改 strict flag 的流程 (rare)

```text
1. PR 修改 base.json
2. 必须 PR description 写 "BREAKING" 前缀
3. 全 workspace typecheck 必须仍通过(consumer 也可能 reject)
4. CI gate: turbo run typecheck --filter=...
5. Reviewer 必须是 libs owner (@vben/tsconfig)
```

## Forbidden

- ❌ 不要把 `strict: false` 设置在 variant —— base 已锁死
- ❌ 不要关掉 `noUncheckedIndexedAccess` —— 索引访问安全
- ❌ 不要添加 `skipLibCheck: false` —— base.json 已 true
- ❌ 不要把 `verbatimModuleSyntax` 关掉 —— 它与 Vite swc plugin 紧耦合
- ❌ 不要用 `any` 作为 workaround —— 用 `unknown` + narrowing
- ❌ 不要在 variant 加 `paths` —— paths 是 app 自己的事
