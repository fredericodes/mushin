import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FileUploadView from '../views/FileUploadView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/encrypt-file',
      name: 'encrypt-file',
      component: FileUploadView
    },
    {
      path: '/decrypt-file',
      name: 'decrypt-file',
      component: FileUploadView
    }
  ]
})

export default router
