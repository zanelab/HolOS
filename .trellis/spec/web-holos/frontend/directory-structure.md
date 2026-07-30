# Web-Holos Directory Structure

> Source layout for `apps/web-holos/`

## 目录树

```
apps/web-holos/
├── package.json
├── index.html                          # vite entry
├── vite.config.ts                      # vite + host/allowedHosts (云端 tunnel 必需)
├── tsconfig.json + tsconfig.node.json  # TS 配
├── public/                             # 静态资源
└── src/
    ├── main.ts                         # 引导(initPreferences + bootstrap)
    ├── bootstrap.ts                    # 异步加载后装载应用
    ├── App.tsx                         # vue 应用入口
    ├── app.vue                         # 顶层组件
    ├── index.css                       # 全局样式
    ├── store/                          # pinia store
    ├── adapter/tdesign.ts              # 适配器
    ├── api/                            # 业务 API
    ├── layouts/                        # 自定义 layout 覆盖
    │   ├── basic.vue                   # 主布局
    │   ├── auth.vue                    # 认证页布局
    │   └── index.ts
    ├── locales/                        # i18n
    │   ├── index.ts
    │   └── langs/
    │       ├── zh-CN/
    │       │   ├── auth.json
    │       │   ├── page.json           # (改过 加 page.home.*)
    │       │   └── demos.json
    │       └── en-US/...
    ├── router/                         # vue-router
    │   ├── index.ts
    │   ├── guard.ts                    # accessToken check + ignoreAccess
    │   ├── access.ts                   # 调 /menu/all API + fallback static menu
    │   └── routes/
    │       ├── core.ts                 # Root / Auth / 404
    │       ├── index.ts                # 动态 + 静态路由聚合
    │       └── modules/                # 每个 module 一个 .ts
    │           └── home.ts
    ├── preferences.ts                  # defineOverridesPreferences
    └── views/
        ├── _core/
        │   ├── about/index.vue
        │   ├── profile/index.vue
        │   ├── authentication/login.vue
        │   └── fallback/not-found.vue
        └── home/index.vue             # 当前起始页(自定)
```

## 约定

- **Layouts**: 覆盖父 layout 时,在 `src/layouts/` 拷一份,basic.vue / auth.vue 改 import 路径
- **Routes**: `core.ts` 加核心路由;业务路由放 `modules/`(vite 自动 glob)
- **i18n**: 在 `preferences.ts` 设 `locale`,在 `locales/langs/<lang>/` 加 json 文件

## 禁止

- ❌ 不要在 `src/views/dashboard/` 等「被删目录」下重建
- ❌ 不要在 `tsconfig.json` 加过松的 strict
