import type { RouteRecordRaw } from 'vue-router';

import { $t } from '#/locales';

const routes: RouteRecordRaw[] = [
  {
    meta: {
      icon: 'lucide:home',
      title: $t('home.title'),
      ignoreAccess: true,
    },
    name: 'HolOSHome',
    path: '/home',
    component: () => import('#/views/home/index.vue'),
  },
];

export default routes;
