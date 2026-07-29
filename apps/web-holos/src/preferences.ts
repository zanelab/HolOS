import { defineOverridesPreferences } from '@vben/preferences';

/**
 * @description 项目配置文件
 * 只需要覆盖项目中的一部分配置，不需要的配置不用覆盖，会自动使用默认配置
 * !!! 更改配置后请清空缓存，否则可能不生效
 */
export const overridesPreferences = defineOverridesPreferences({
  // overrides
  app: {
    name: import.meta.env.VITE_APP_TITLE,
    defaultHomePath: '/home',
    loginRequired: false,
    layout: 'mixed-nav', // 'header-nav' | 'sidebar-nav' | 'mixed-nav' | 'header-mixed-nav' | 'header-sidebar-nav' | 'sidebar-mixed-nav' | 'full-content'
    // mixed-nav: 头部菜单 + 侧边栏混合 — 既能看到顶部菜单也能看到侧栏
  },
});
