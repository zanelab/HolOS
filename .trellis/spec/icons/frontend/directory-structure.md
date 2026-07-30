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
- **Tree-shaking**: import specific icons
- **Auto-import**: via unplugin-vue-components

## 禁止

- Don't bundle the full Iconify icon set
- Don't add inline <svg> in templates
- Don't import icons from react-icons
