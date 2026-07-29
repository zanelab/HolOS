import type {
  ComponentRecordType,
  GenerateMenuAndRoutesOptions,
} from '@vben/types';

import type { RouteRecordStringComponent } from '@vben/types';

import { generateAccessible } from '@vben/access';
import { preferences } from '@vben/preferences';

import { message } from '#/adapter/tdesign';
import { getAllMenusApi } from '#/api';
import { BasicLayout, IFrameView } from '#/layouts';
import { $t } from '#/locales';

const forbiddenComponent = () => import('#/views/_core/fallback/forbidden.vue');

/**
 * HolOS 静态 fallback 菜单(API 失败时使用)
 * 保证即使未登录 / token 过期 / API 不可用,侧栏仍有可见的"首页"菜单
 */
const FALLBACK_MENUS: RouteRecordStringComponent[] = [
  {
    component: 'BasicLayout',
    meta: {
      icon: 'lucide:home',
      title: $t('page.home.title'),
      order: 1,
    },
    name: 'HolOSHome',
    path: '/home',
  },
] satisfies RouteRecordStringComponent[];

async function generateAccess(options: GenerateMenuAndRoutesOptions) {
  const pageMap: ComponentRecordType = import.meta.glob('../views/**/*.vue');

  const layoutMap: ComponentRecordType = {
    BasicLayout,
    IFrameView,
  };

  return await generateAccessible(preferences.app.accessMode, {
    ...options,
    fetchMenuListAsync: async () => {
      message.loading({
        content: `${$t('common.loadingMenu')}...`,
        duration: 1500,
      });
      try {
        const list = await getAllMenusApi();
        // 如果 API 返回有效菜单,使用之;否则回落到静态 home
        return Array.isArray(list) && list.length > 0 ? list : FALLBACK_MENUS;
      } catch {
        // API 调用失败(未登录 / token 过期 / 网络问题)
        // 使用静态 fallback
        return FALLBACK_MENUS;
      }
    },
    // 可以指定没有权限跳转403页面
    forbiddenComponent,
    // 如果 route.meta.menuVisibleWithForbidden = true
    layoutMap,
    pageMap,
  });
}

export { generateAccess };
