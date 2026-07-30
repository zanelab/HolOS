# @vben/styles Component Guidelines

> Pure CSS package. Apps consume styles via Tailwind utility classes.

## 模式: app-level CSS with framework imports

```css
/* apps/web-antd/src/index.css */
@import url('@vben/styles/index');
/* plus app-specific overrides */
```

## 禁止

- Don't mix framework CSS in same file
- 不要重新定义 Tailwind tokens
