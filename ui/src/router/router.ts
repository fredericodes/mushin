import { createRouter, createWebHistory } from 'vue-router'
import HomeComponent from '../components/HomeComponent.vue'
import FileUploadComponent from '../components/FileUploadComponent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeComponent
    },
    {
      path: '/encrypt-file',
      name: 'encrypt-file',
      component: FileUploadComponent
    },
    {
      path: '/decrypt-file',
      name: 'decrypt-file',
      component: FileUploadComponent
    }
  ]
})

export default router
