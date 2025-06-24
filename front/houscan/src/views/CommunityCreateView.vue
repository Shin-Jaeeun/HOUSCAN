<template>
  <div class="create-page mt-5 pt-5">
    <!-- 🔙 목록으로 돌아가기 버튼 (폼 밖 상단에 배치) -->
    <RouterLink to="/community" class="cancel-top-btn">← 글쓰기 취소하기</RouterLink>
    <h2 class="fw-bold">새 글 작성</h2>

    <div v-if="isLogin" class="form-wrapper">
      <form @submit.prevent="createPost" class="form-box">
        <!-- 🔹 카테고리 선택 -->
        <div class="form-group">
          <label for="category">카테고리</label>
          <select id="category" v-model="category" required>
            <option disabled value="">카테고리를 선택하세요</option>
            <option v-for="cat in categoryOptions" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>

        <!-- 🔹 제목 -->
        <div class="form-group">
          <label for="title">제목</label>
          <input id="title" type="text" v-model="title" required />
        </div>

        <!-- 🔹 내용 -->
        <div class="form-group">
          <label for="content">내용</label>
          <textarea id="content" v-model="content" rows="8" required></textarea>
        </div>

        <!-- 🔹 작성 완료 버튼 -->
        <div class="form-actions">
          <button type="submit">작성 완료</button>
        </div>
      </form>
    </div>

    <p v-else class="login-warning">※ 로그인 후에 작성 가능합니다.</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/useAuthStore'

const router = useRouter()
const authStore = useAuthStore()
const isLogin = computed(() => authStore.isLogin)

const title = ref('')
const content = ref('')
const category = ref('')

// 🔹 카테고리 옵션 목록
const categoryOptions = ['아파트', '임의공급', '주택', '토지', '상가', '예적금', '자유게시판']

const createPost = async () => {
  try {
    const res = await axios.post(
      'http://localhost:8000/api/v1/community/posts/',
      {
        category: category.value,
        title: title.value,
        content: content.value
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      }
    )
    router.push(`/community/${res.data.id}`)
  } catch (err) {
    console.error('❌ 게시글 작성 실패:', err)
  }
}
</script>

<style scoped>

.create-page {
  max-width: 700px;
  margin: auto;
  padding: 2rem;
}

.cancel-top-btn {
  display: inline-block;
  margin-bottom: 1rem;
  color: #f37075;
  text-decoration: underline;
  font-size: 0.95rem;
}
.cancel-top-btn:hover {
  text-decoration: none;
  color: #d9534f;
}

.form-wrapper {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

button {
  padding: 0.5rem 1.2rem;
  background-color: #f37075;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
}

.login-warning {
  color: #999;
  margin-top: 1rem;
}
</style>