<template>
  <div class="signup-wrapper">
    <!-- 왼쪽 문구 -->
    <div class="left-panel">
      <div class="slogan-box">
        <h1 class="slogan">
          내 집 마련, <span class="highlight">HOUSCAN</span>과 함께<br />
          시작해보시죠.
        </h1>
      </div>
    </div>

    <!-- ✅ 회원가입 폼 -->
    <div class="right-panel">
      <h2 class="fw-bold py-3">회원가입</h2>
      <form @submit.prevent="submitSignup">
        <!-- 닉네임 -->
        <input v-model="username" type="text" placeholder="닉네임" required />

        <!-- 이메일 + 중복 확인 -->
        <div class="email-group">
          <input v-model="email" type="email" placeholder="이메일" required />
          <button type="button" @click="checkEmail">중복 확인</button>
        </div>
        <div class="email-check-message">
          <span v-if="emailChecked && !emailExists">✅ 사용 가능</span>
          <span v-if="emailExists">❌ 중복됨</span>
        </div>

        <!-- 인증 메일 보내기 -->
        <div v-if="!emailExists && emailChecked">
          <button type="button" @click="sendCode">인증 메일 보내기</button>
        </div>

        <!-- 인증번호 입력 -->
        <div v-if="verificationCodeSent">
          <input v-model="code" placeholder="인증번호 입력" />
          <button type="button" @click="verifyCode">확인</button>
          <span v-if="verified">✅ 인증 완료</span>
        </div>

        <!-- 생년월일 -->
        <input v-model="birthdate" type="date" placeholder="생년월일" required />

        <!-- 비밀번호 -->
        <input v-model="password" type="password" placeholder="비밀번호" required />

        <!-- 비밀번호 확인 -->
        <input v-model="confirmPassword" type="password" placeholder="비밀번호 확인" required />
        <span v-if="confirmPassword && confirmPassword !== password">❌ 불일치</span>
        <span v-if="confirmPassword && confirmPassword === password">✅ 일치</span>

        <button type="submit" :disabled="!canSubmit">가입하기</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import JSConfetti from 'js-confetti'

const jsConfetti = new JSConfetti()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const birthdate = ref('')

const emailChecked = ref(false)
const emailExists = ref(false)
const verificationCodeSent = ref(false)
const code = ref('')
const verified = ref(false)

const checkEmail = async () => {
  const res = await axios.get(`http://localhost:8000/api/v1/accounts/email-check/?email=${email.value}`)
  emailChecked.value = true
  emailExists.value = res.data.exists
}

const sendCode = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/accounts/send-code/', {
      email: email.value
    })
    verificationCodeSent.value = true
    alert('이메일로 인증번호를 보냈습니다!')
    console.log('✅ 인증번호 전송 성공:', res.data)
  } catch (err) {
    console.error('❌ 인증번호 전송 실패:', err)
    alert('인증 메일 전송 중 오류 발생')
  }
}

const verifyCode = async () => {
  const res = await axios.post('http://localhost:8000/api/v1/accounts/verify-code/', {
    email: email.value,
    code: code.value,
  })
  if (res.data.verified) {
    verified.value = true
    alert('인증 성공!')
  } else {
    alert('인증 실패')
  }
}

const canSubmit = computed(() => {
  return (
    username.value &&
    email.value &&
    emailChecked.value &&
    !emailExists.value &&
    verified.value &&
    birthdate.value &&
    password.value &&
    confirmPassword.value &&
    password.value === confirmPassword.value
  )
})

const submitSignup = async () => {
  try {
    await axios.post('http://localhost:8000/api/v1/accounts/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      birthdate: birthdate.value,
    })

    const loginRes = await axios.post('http://localhost:8000/api/v1/accounts/login/', {
      email: email.value,
      password: password.value,
    })

    localStorage.setItem('access', loginRes.data.access)
    localStorage.setItem('refresh', loginRes.data.refresh)

    // ✅ 회원가입 후 폭죽
    jsConfetti.addConfetti({
      emojis: ['🎉', '🎊', '✨', '💚'],
      emojiSize: 30,
      confettiNumber: 80
    })

    alert('회원가입 완료!')
    router.push('/')
  } catch (err) {
    alert('회원가입 실패')
    console.error(err)
  }
}
</script>

<style scoped>
.signup-wrapper {
  display: flex;
  height: calc(100vh - 80px);
  background-image: url('@/assets/main-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 0 8vw; /* ✅ 여백 확장 */
  gap: 20rem; /* ✅ 간격 추가 */
}

.signup-wrapper::before {
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

/* ✅ 슬로건 */
.left-panel {
  position: relative;
  z-index: 1;
  flex: 1;
  max-width: 600px;
}

.slogan-wrapper {
  text-align: left;
  z-index: 1;
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

/* ✅ 폼 */
.right-panel {
  position: relative;
  width: 420px;
  min-height: 520px;
  background-color: #ffffffee;
  padding: 2.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 1;
}

.right-panel h2 {
  font-family: 'Pretendard', sans-serif;
  font-size: 1.4rem;
  color: #333;
  margin-top: 0;
  margin-bottom: 2rem;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

input {
  padding: 0.6rem;
  font-size: 0.95rem;
  border-radius: 0;
  border: 1px solid #ccc;
}

button {
  padding: 0.6rem;
  font-size: 1rem;
  background-color: #2F9E44;
  border: none;
  border-radius: 0;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

/* ✅ 가입하기 버튼만 색상 변경 */
button[type="submit"] {
  background-color: #f37075;
}

button[disabled] {
  background-color: #ccc;
  cursor: not-allowed;
}

.email-group {
  display: flex;
  gap: 0.5rem;
}

.email-group input {
  flex: 1;
}

.email-check-message {
  font-size: 0.85rem;
  margin-top: -0.4rem;
  margin-bottom: 0.5rem;
  color: #2F9E44;
}
</style>
