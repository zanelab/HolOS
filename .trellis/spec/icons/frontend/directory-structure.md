# @vben/icons Directory Structure

> Iconify + SVG icons. Used across all web-* apps.

## 目录树 (verified)

```
@vben/icons/
├── package.json                # name "@vben/icons" v5.7.0
├── index.ts                    # re-exports Svg*Icon + IconifyIcon
└── svg/
    ├── SvgAntdvLogoIcon.vue
    ├── SvgAntdvNextLogoIcon.vue
    └── (... per-component SVG icons)
```

## 约定

- **<IconifyIcon :icon="name">** - runtime-loaded from Iconify API
- **<SvgFooIcon>** - local SVG components
- **Tree-shaking**：只 import 具体图标
- **自动 import**：通过 unplugin-vue-components

## 禁止

- 不要打包完整 Iconify 图标集
- 不要在模板中嵌入 <svg>
- 不要从 react-icons 导入图标
