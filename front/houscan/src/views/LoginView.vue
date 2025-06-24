<template>
  <div class="login-wrapper">
    <!-- ✅ 슬로건 영역 -->
    <div class="left-panel">
      <div class="slogan-wrapper">
        <h1 class="slogan">
          <span class="highlight">HOUSCAN</span>으로
          <br> 당신만의 맞춤형 청약 전략을 <br>시작하세요 !
        </h1>
      </div>
    </div>

    <!-- ✅ 로그인 폼 -->
    <div class="right-panel">
      <h2 class="fw-bold">로그인</h2>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="이메일" required />
        <input v-model="password" type="password" placeholder="비밀번호" required />
        <button type="submit" class="fw-bold">로그인</button>
      </form>
      <div class="login-links fw-semibold">
        <RouterLink to="/login/find">비밀번호를 잊으셨나요?</RouterLink>
        <RouterLink to="/signup">아직 회원이 아니신가요?</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const email = ref('')
const password = ref('')
const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/login/', {
      email: email.value,
      password: password.value,
    })

    localStorage.setItem('accessToken', res.data.access)
    localStorage.setItem('refresh', res.data.refresh)

    authStore.setLogin({
      username: res.data.username,
      email: res.data.email,
    })

    router.push('/')
  } catch (err) {
    alert('로그인 실패')
  }
}
</script>

<style scoped>

.login-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 80px);
  background-image: url('@/assets/main-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 0 6vw;
  gap: 20rem; /* ✅ 간격 더 넓힘 */
  position: relative;
}

.login-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/main-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: grayscale(40%) brightness(0.6);
  z-index: 0;
}

.left-panel {
  position: relative;
  z-index: 1;
  max-width: 500px;
  flex: 1;
}

.slogan-wrapper {
  text-align: left;
  z-index: 1;
  gap : 10rem
}

.slogan {
  font-size: 2.5rem;
  line-height: 1.6;
  color: white;
  font-family: 'Pretendard', sans-serif;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
  margin: 0;
}

.highlight {
  color: #A1F0A1;
  font-weight: bold;
}

.right-panel {
  position: relative;
  width: 420px;
  min-height: 420px;
  background-color: #EEEEEE;
  padding: 3rem;
  border-radius: 0.5rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1;
}

.right-panel h2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 1.4rem;
  color: #333;
  margin-top: 0;
  margin-bottom: 3rem;
  text-align: center;
  align-self: center;
  width: 100%;
}

.right-panel form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  width: 100%;
  flex-grow: 1;
}

.right-panel input {
  padding: 0.6rem;
  font-size: 0.95rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.right-panel input::placeholder {
  color: #999;
  font-size: 0.95rem;
}

.right-panel button {
  margin-top: 1rem;
  padding: 0.85rem;
  font-size: 1.05rem;
  background-color: #2F9E44;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.right-panel button:hover {
  background-color: #276f3d;
}

.login-links {
  margin-top: auto;
  padding-top: 0.8rem;
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  width: 100%;
}

.login-links a {
  color: #E55050;
  text-decoration: none;
  font-weight: 500;
}

.login-links a:hover {
  text-decoration: underline;
}
</style>
