<template>
  <div class="update-wrapper">
    <h2 class="title fw-bold py-5">회원정보 수정</h2>
    <h3 class="subtitle py-3">📋 HOUSCAN과 함께 정보를 안전하게 관리하세요.</h3>

    <!-- 탭 전환 버튼 -->
    <div class="tabs">
      <button :class="{ active: mode === 'nickname' }" @click="mode = 'nickname'">닉네임 변경</button>
      <button :class="{ active: mode === 'password' }" @click="mode = 'password'">비밀번호 변경</button>
    </div>

    <!-- 닉네임 변경 섹션 -->
    <section v-if="mode === 'nickname'" class="box-section position-relative">
      <h3 class="fw-semibold">🧑 닉네임 변경</h3>
      <p class="guide-text">닉네임은 최대 10자까지 입력 가능합니다.</p>
      <form @submit.prevent="updateNickname">
        <label>📧 이메일
          <input type="email" :value="user.email" readonly />
        </label>
        <label>✏️ 새 닉네임
          <input v-model="username" type="text" placeholder="변경할 닉네임" />
        </label>
        <label>🔒 비밀번호 확인
          <input v-model="passwordForName" type="password" placeholder="비밀번호 입력" />
        </label>
        <button type="submit">닉네임 변경</button>
      </form>
    </section>

    <!-- 비밀번호 변경 섹션 -->
    <section v-else class="box-section position-relative">
      <h3>🔐 비밀번호 변경</h3>
      <p class="guide-text">보안을 위해 새 비밀번호를 확인해주세요.</p>
      <form @submit.prevent="updatePassword">
        <label>🔑 기존 비밀번호
          <input v-model="currentPassword" type="password" placeholder="현재 비밀번호 입력" />
        </label>
        <label>🆕 새 비밀번호
          <input v-model="newPassword" type="password" placeholder="새 비밀번호" />
        </label>
        <label>✅ 새 비밀번호 확인
          <input v-model="confirmNewPassword" type="password" placeholder="새 비밀번호 확인" />
        </label>
        <button type="submit">비밀번호 변경</button>
      </form>
    </section>

    <!-- ✅ 회원탈퇴 버튼 -->
    <div class="withdraw-box">
      <hr />
      <button class="withdraw-btn" @click="showInlineModal = true">회원탈퇴</button>
    </div>

    <!-- ✅ 탈퇴 모달 -->
    <div v-if="showInlineModal" class="custom-modal-overlay">
      <div class="custom-modal">
        <h5>회원 탈퇴 확인</h5>
        <p>계정 보호를 위해 비밀번호를 다시 입력해주세요.</p>
        <input
          v-model="withdrawPassword"
          type="password"
          placeholder="비밀번호 입력"
          class="form-control"
        />
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showInlineModal = false">취소</button>
          <button class="btn btn-danger" @click="handleWithdraw">탈퇴하기</button>
        </div>
      </div>
    </div>

    <!-- ✅ 성공 메시지 모달 -->
    <div v-if="showSuccessModal" class="custom-modal-overlay">
      <div class="custom-modal">
        <h5>✅ 변경 완료</h5>
        <p>{{ successMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()

const mode = ref('nickname')
const user = ref({ email: '', username: '' })
const username = ref('')
const passwordForName = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')
const withdrawPassword = ref('')
const showInlineModal = ref(false)
const showSuccessModal = ref(false)
const successMessage = ref('')

onMounted(async () => {
  const token = localStorage.getItem('access')
  const res = await axios.get('http://localhost:8000/api/v1/accounts/me/', {
    headers: { Authorization: `Bearer ${token}` }
  })
  user.value = res.data
})

const showModalAndRedirect = (message) => {
  successMessage.value = message
  showSuccessModal.value = true
  setTimeout(() => {
    showSuccessModal.value = false
    router.push('/')
  }, 1000)
}

const updateNickname = async () => {
  try {
    const token = localStorage.getItem('accessToken')
    await axios.put('http://localhost:8000/api/v1/accounts/update-nickname/', {
      username: username.value,
      password: passwordForName.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    authStore.username = username.value
    showModalAndRedirect('닉네임이 성공적으로 변경되었습니다!')
  } catch (err) {
    alert('닉네임 변경 실패: ' + (err.response?.data?.detail || JSON.stringify(err.response?.data || err)))
  }
}

const updatePassword = async () => {
  if (newPassword.value !== confirmNewPassword.value) {
    alert('새 비밀번호와 확인이 일치하지 않습니다.')
    return
  }
  try {
    const token = localStorage.getItem('accessToken')
    await axios.put('http://localhost:8000/api/v1/accounts/update-password/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    showModalAndRedirect('비밀번호가 성공적으로 변경되었습니다!')
  } catch (err) {
    alert('비밀번호 변경 실패: ' + (err.response?.data?.detail || JSON.stringify(err.response?.data || err)))
  }
}

const handleWithdraw = async () => {
  if (!withdrawPassword.value) {
    alert('비밀번호를 입력해주세요.')
    return
  }
  try {
    const token = localStorage.getItem('accessToken')
    await axios.delete('http://localhost:8000/api/v1/accounts/delete/', {
      headers: { Authorization: `Bearer ${token}` },
      data: { password: withdrawPassword.value }
    })
    alert('회원탈퇴가 완료되었습니다.')
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refresh')
    router.push('/login')
  } catch (err) {
    alert('회원탈퇴 실패: ' + (err.response?.data?.detail || JSON.stringify(err.response?.data || err)))
  } finally {
    showInlineModal.value = false
    withdrawPassword.value = ''
  }
}
</script>

<style scoped>
.update-wrapper {
  max-width: 960px;
  margin: 0 auto;
  padding-top: 6rem;
  padding-bottom: 5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(to bottom, #ffffff, #f9fafb);
  min-height: 100vh;
}

.title {
  font-size: 3rem;
  color: #000;
  text-align: center;
  font-family: 'Pretendard', sans-serif;
  margin-bottom: 0.2rem;
}

.subtitle {
  font-size: 1rem;
  text-align: center;
  color: #666;
  margin-bottom: 1.5rem;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.tabs button {
  background: white;
  border: 2px solid #f37075;
  color: #f37075;
  padding: 0.5rem 1.2rem;
  border-radius: 2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tabs .active {
  background-color: #f37075;
  color: white;
}

.box-section {
  background: #fff;
  border-radius: 1rem;
  padding: 3rem 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 720px;
}

h3 {
  font-size: 1.4rem;
  font-weight: 600;
  color: #333;
}

.guide-text {
  font-size: 0.9rem;
  color: #777;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

label {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 0.2rem;
}

input {
  padding: 1.2rem;
  font-size: 1.15rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 0.4rem;
  width: 100%;
}

button[type="submit"] {
  padding: 0.8rem;
  font-size: 1.1rem;
  background-color: #f37075;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #cc4e56;;
}

.withdraw-box {
  margin-top: 2rem;
  text-align: center;
}

.withdraw-btn {
  font-size: 0.95rem;
  color: #d32f2f;
  background: none;
  border: none;
  cursor: pointer;
  text-align: center;
  text-decoration: underline;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.modal p {
  font-size: 0.95rem;
  margin-bottom: 1rem;
  color: #444;
}

.modal-input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.confirm-btn {
  flex: 1;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  font-weight: bold;
  cursor: pointer;
}

.cancel-btn {
  flex: 1;
  background-color: #ccc;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1rem;
  font-weight: bold;
  cursor: pointer;
}

.custom-modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
}

.custom-modal {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  z-index: 21;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

input[readonly] {
  background-color: #f1f3f5;  /* 밝은 회색 */
  color: #495057;             /* 어두운 텍스트 */
  cursor: not-allowed;
}

.custom-modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.custom-modal {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

</style>
