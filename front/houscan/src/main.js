// main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

// ✅ Bootstrap만 추가
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'  // JS 컴포넌트(모달, 드롭다운 등) 쓸 때 필요

// ✅ axios 기본 주소 설정
axios.defaults.baseURL = 'http://localhost:8000'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
