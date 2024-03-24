import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import 'vue3-toastify/dist/index.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify';

const app = createApp(App)

app.use(router)

app.use(Vue3Toastify, {
    autoClose: 1500,
    position: "bottom-left",
    pauseOnHover: false,
    hideProgressBar: true
} as ToastContainerOptions);

app.mount('#app')
