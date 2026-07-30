# @vben/tsconfig "Component" Style — Config Variants

> 无 Vue 组件。 "Components" are typed config objects (the 5 `.json` variants
> exposed under `internal/tsconfig/`). Source verified against the v5.7.0 file set.

## 模式: 每个 variant 是 typed JSON object

`base.json` (verified) 是其他所有 variant 的根:

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Base",
  "compilerOptions": {
    "composite": false,
    "target": "ESNext",
    "moduleDetection": "force",
    "experimentalDecorators": true,
    "module": "ESNext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "strict": true,
    "strictNullChecks": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitAny": true,
    "noImplicitOverride": true,
    "noImplicitThis": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "inlineSources": false,
    "noEmit": true,
    "removeComments": true,
    "sourceMap": false,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "preserveWatchOutput": true
  },
  "exclude": ["**/node_modules/**", "**/dist/**", "**/.turbo/**"]
}
```

## 各 variant 的具体 "契约"

`web.json` (verified) — web 包默认:

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Web Package",
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "preserve",
    "jsxImportSource": "vue",
    "lib": ["ESNext", "DOM", "DOM.Iterable"],
    "useDefineForClassFields": true,
    "moduleResolution": "bundler",
    "types": ["vite/client"],
    "declaration": false
  }
}
```

`web-app.json` (verified) — 实际 app 的延伸:

```jsonc
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "display": "Web Application",
  "extends": "./web.json",
  "compilerOptions": {
    "types": ["vite/client", "@vben/types/global"]
  }
}
```

## Conventions

- **`display` 必填** —— tsconfig tool 会展示这个 `display` 字段
- **`$schema` 必填** —— 帮助 IDE 智能提示
- **`extends` 用相对路径** —— 不引用包,因为不被 publish
- **数组字面量多行** —— 字段多时,每个 option 占一行便于 diff
- **不要继承第三方 tsconfig** —— 只继承本包内其他 variant

## Naming

- variant 名是 kebab-case (`web-app`, 不用 `webApp`)
- field 名是 camelCase (`moduleResolution`, 不用 `module-resolution`)
- value 是 string 时 用双引号(`"ESNext"`)

## Forbidden

- ❌ 不要复制 base.json 的 `compilerOptions.*` 到 variant —— extends 已生效
- ❌ 不要在 variant 里再次设置 `strict` —— 已由 base.json 强制为 true
- ❌ 不要把 `noUncheckedIndexedAccess: true` 关掉 —— base.json 一律开启
- ❌ 不要写 `tsconfig.json` 顶层文件 ——
  IDE 会和 variant 冲突,且本包不发 npm
- ❌ 不要使用 `template` 字段(ts 5.6+ 已弃用,且 5.7.0 不需要)
- ❌ 不要新增 `.d.ts` 进入此包 ——
  全局 type 在 `@vben/types/global`
