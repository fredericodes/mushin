import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FileEncryptionUploadView from '../views/FileEncryptionUploadView.vue'
import FileDecryptionUploadView from '../views/FileDecryptionUploadView.vue'
import TrackEncryptionView from '../views/TrackEncryptionView.vue'
import TrackDecryptionView from '../views/TrackDecryptionView.vue'

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
    },
    {
      path: '/track-encryption',
      name: 'track-encryption',
      component: TrackEncryptionView
    },
    {
      path: '/track-decryption',
      name: 'track-decryption',
      component: TrackDecryptionView
    },
  ]
})

export default router
