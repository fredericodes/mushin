import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FileEncryptionUploadView from '../views/FileEncryptionUploadView.vue'
import FileDecryptionUploadView from '../views/FileDecryptionUploadView.vue'

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
      component: FileEncryptionUploadView
    },
    {
      path: '/decrypt-file',
      name: 'decrypt-file',
      component: FileDecryptionUploadView
    }
  ]
})

export default router
