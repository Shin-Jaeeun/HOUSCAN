<template>
  <div class="find-wrapper">
    <div class="content-box">
      <!-- 왼쪽: 슬로건 -->
      <div class="left-panel">
        <h1 class="slogan">
          잠시 잊었을 뿐이에요. 😔 <br> 다시 이어갈 수 있어요.
        </h1>
      </div>

      <!-- 오른쪽: 폼 -->
      <div class="right-panel">
        <h2 class="fw-bold">비밀번호 재설정</h2>

        <!-- 이메일 확인 단계 -->
        <form v-if="!emailVerified" @submit.prevent="checkEmail">
          <input v-model="email" type="email" placeholder="이메일" required />
          <button type="submit">이메일 확인</button>

          <div v-if="emailChecked && emailExists" class="check-message">
            ✅ 이메일 확인됨
          </div>

          <div v-else-if="emailChecked && !emailExists" class="not-found-box">
            ❌ 존재하지 않는 이메일입니다.
            <RouterLink to="/signup" class="signup-link">회원가입하러 가기</RouterLink>
          </div>
        </form>

        <!-- 비밀번호 변경 단계 -->
        <form v-else @submit.prevent="resetPassword">
          <input v-model="newPassword" type="password" placeholder="새 비밀번호" required />
          <input v-model="confirmPassword" type="password" placeholder="비밀번호 확인" required />
          <button type="submit" :disabled="newPassword !== confirmPassword">비밀번호 재설정</button>

          <span v-if="confirmPassword && newPassword !== confirmPassword">❌ 불일치</span>
          <span v-if="confirmPassword && newPassword === confirmPassword">✅ 일치</span>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const emailChecked = ref(false)
const emailExists = ref(false)
const emailVerified = ref(false)
const router = useRouter()

const checkEmail = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/accounts/email-check/?email=${email.value}`)
  emailChecked.value = true
  emailExists.value = res.data.exists
  emailVerified.value = res.data.exists
}

const resetPassword = async () => {
  try {
    await axios.put('http://localhost:8000/api/v1/accounts/reset-password/', {
      email: email.value,
      password: newPassword.value
    })
    alert('비밀번호가 성공적으로 변경되었습니다.')
    router.push('/login')
  } catch (err) {
    alert('비밀번호 변경 실패')
  }
}
</script>

<style scoped>
.find-wrapper {
  height: calc(100vh - 80px);
  background-image: url('@/assets/main-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.find-wrapper::before {
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

.content-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rem;
  z-index: 1;
}

.left-panel {
  max-width: 480px;
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
  width: 400px;
  background-color: #ffffffee;
  padding: 2.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.right-panel h2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 1.4rem;
  color: #333;
  margin-top: 0;
  margin-bottom: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  width: 100%;
}

input {
  padding: 0.6rem;
  font-size: 0.95rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  padding: 0.6rem;
  font-size: 1rem;
  background-color: #2F9E44;
  border: none;
  border-radius: 4px;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.not-found-box {
  font-size: 0.9rem;
  margin-top: 0.5rem;
  color: #c62828;
  font-weight: 500;
}

.signup-link {
  display: inline-block;
  margin-top: 0.3rem;
  color: #2F9E44;
  text-decoration: underline;
  font-size: 0.95rem;
}

.check-message {
  font-size: 0.9rem;
  color: #2F9E44;
  margin-top: 0.4rem;
}
</style>