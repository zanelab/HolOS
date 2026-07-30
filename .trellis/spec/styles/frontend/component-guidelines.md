# @vben/styles Component Guidelines

> Pure CSS package. Apps consume styles via Tailwind utility classes.

## Pattern: app-level CSS with framework imports

```css
/* apps/web-antd/src/index.css */
@import url('@vben/styles/index');
/* plus app-specific overrides */
```

## Forbidden

- Don't mix framework CSS in same file
- Don't redefine Tailwind tokens
