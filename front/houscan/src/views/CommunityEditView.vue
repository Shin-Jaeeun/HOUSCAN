<template>
  <div class="edit-page mt-5 pt-5">
    <!-- 🔙 목록으로 돌아가기 버튼 (상단) -->
    <RouterLink to="/community" class="cancel-top-btn">← 글수정 취소하기</RouterLink>
    <h2 class="fw-bold">게시글 수정</h2>

    <div v-if="isLogin && isOwner" class="form-wrapper">
      <form @submit.prevent="updatePost" class="form-box">
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

        <!-- 🔹 수정 완료 버튼 -->
        <div class="form-actions">
          <button type="submit">수정 완료</button>
        </div>
      </form>
    </div>

    <p v-else-if="!isLogin" class="login-warning">※ 로그인 후 접근 가능합니다.</p>
    <p v-else class="warning">※ 본인만 수정할 수 있습니다.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/useAuthStore'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLogin = computed(() => authStore.isLogin)
const username = computed(() => authStore.username)

const postId = route.params.postId
const title = ref('')
const content = ref('')
const category = ref('')
const postUser = ref('')
const isOwner = computed(() => postUser.value === username.value)

const categoryOptions = ['아파트', '임의공급', '주택', '토지', '상가', '예적금', '자유게시판']

// 기존 게시글 로딩
const fetchPost = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/community/posts/${postId}/`)
    title.value = res.data.title
    content.value = res.data.content
    category.value = res.data.category
    postUser.value = res.data.user
  } catch (err) {
    console.error('❌ 게시글 불러오기 실패:', err)
  }
}

// 수정 요청
const updatePost = async () => {
  try {
    await axios.put(
      `http://localhost:8000/api/v1/community/posts/${postId}/`,
      {
        title: title.value,
        content: content.value,
        category: category.value
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      }
    )
    router.push(`/community/${postId}`)
  } catch (err) {
    console.error('❌ 수정 실패:', err)
  }
}

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.edit-page {
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

.login-warning,
.warning {
  color: #999;
  margin-top: 1rem;
}
</style>
