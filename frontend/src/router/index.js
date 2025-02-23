import { createRouter, createWebHistory } from 'vue-router';
import Section1 from '@/views/Section1.vue';
import Section2 from '@/views/Section2.vue';

const routes = [
  { path: '/', component: Section1 },
  { path: '/Section2', component: Section2 }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
