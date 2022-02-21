import { createApp } from 'vue'
import './assets/global.css'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

import App from './App.vue'
import router from './router/router'

const app = createApp(App)

app.use(VueSweetalert2);

app.use(router)

app.mount('#app')
