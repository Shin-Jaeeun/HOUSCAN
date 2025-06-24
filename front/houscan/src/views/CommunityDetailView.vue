<template>
  <div class="community-detail">
    <RouterLink to="/community" class="back-link">← 목록으로</RouterLink>

    <div class="AddWrap">
      <table class="tbAdd">
        <colgroup>
          <col width="15%" />
          <col width="*" />
        </colgroup>
        <tbody>
          <tr>
            <th>제목</th>
            <td>
              {{ post?.title }}
              <span v-if="post?.user === username" class="post-actions">
                <RouterLink :to="`/community/${postId}/edit`" class="edit-btn" title="수정">✏️</RouterLink>
                <button @click="deletePost" class="delete-btn" title="삭제">🗑</button>
              </span>
            </td>
          </tr>
          <tr>
            <th>카테고리</th>
            <td>{{ post?.category }}</td>
          </tr>
          <tr>
            <th>작성자</th>
            <td>{{ post?.user }}</td>
          </tr>
          <tr>
            <th>작성일</th>
            <td>{{ formatDate(post?.created_at) }}</td>
          </tr>
          <tr>
            <th>내용</th>
            <td class="txt_cont" v-html="formattedContent"></td>
          </tr>
        </tbody>
      </table>

      <div class="like-wrapper">
        <button class="like-btn" @click="toggleLike" :disabled="!isLogin">
          {{ liked ? '❤️' : '🤍' }} {{ likeCount }}
        </button>
        <span v-if="!isLogin" class="login-warning">＊ 로그인 시 좋아요 가능</span>
      </div>
    </div>

    <div class="comment-section">
      <h3>💬 댓글</h3>
      <ul class="comment-list">
        <li v-for="comment in comments" :key="comment.id" class="comment-card">
          <div class="comment-header">
            <strong>{{ comment.username }}</strong>
            <button v-if="isCommentDeletable(comment)" @click="deleteComment(comment.id)" class="comment-delete">
              삭제
            </button>
          </div>
          <p class="comment-content">{{ comment.content }}</p>
          <p class="comment-date">{{ formatDate(comment.created_at) }}</p>
        </li>
      </ul>

      <div v-if="isLogin" class="comment-form">
        <textarea v-model="newComment" placeholder="댓글을 입력하세요" rows="3" @keydown.enter.exact.prevent="submitComment" />
        <button @click="submitComment">댓글 작성</button>
      </div>
      <p v-else class="login-warning">＊ 로그인 시 댓글 작성 가능</p>
    </div>
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
const post = ref(null)
const formattedContent = ref('')
const comments = ref([])
const newComment = ref('')

const liked = ref(false)
const likeCount = ref(0)

const fetchPost = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/community/posts/${postId}/`)
    post.value = res.data
    formattedContent.value = res.data.content.replace(/(?:\r\n|\r|\n)/g, '<br />')
    likeCount.value = res.data.like_count ?? 0
    liked.value = res.data.is_liked ?? false
  } catch (err) {
    console.error('❌ 게시글 로드 실패:', err)
  }
}

const fetchComments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/community/posts/${postId}/comments/`)
    comments.value = res.data
  } catch (err) {
    console.error('❌ 댓글 로드 실패:', err)
  }
}

const submitComment = async () => {
  const token = authStore.accessToken || localStorage.getItem('accessToken')
  if (!token || !newComment.value.trim()) return

  try {
    await axios.post(
      `http://localhost:8000/api/v1/community/posts/${postId}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    newComment.value = ''
    fetchComments()
  } catch (err) {
    console.error('❌ 댓글 작성 실패:', err)
  }
}

const deleteComment = async (commentId) => {
  const token = authStore.accessToken || localStorage.getItem('accessToken')
  if (!token) return

  try {
    await axios.delete(`http://localhost:8000/api/v1/community/posts/${postId}/comments/${commentId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    fetchComments()
  } catch (err) {
    console.error('❌ 댓글 삭제 실패:', err)
  }
}

const deletePost = async () => {
  const token = authStore.accessToken || localStorage.getItem('accessToken')
  if (!token) return

  try {
    await axios.delete(`http://localhost:8000/api/v1/community/posts/${postId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    router.push('/community')
  } catch (err) {
    console.error('❌ 게시글 삭제 실패:', err)
  }
}

const toggleLike = async () => {
  const token = authStore.accessToken || localStorage.getItem('accessToken')
  if (!token) return

  try {
    await axios.post(`http://localhost:8000/api/v1/community/posts/${postId}/like/`, {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    liked.value = !liked.value
    likeCount.value += liked.value ? 1 : -1
  } catch (err) {
    console.error('❌ 좋아요 실패:', err)
  }
}

const isCommentDeletable = (comment) => {
  return comment.username === username.value || post.value.user === username.value
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleString()
}

onMounted(() => {
  fetchPost()
  fetchComments()
})
</script>


<style scoped>
.community-detail {
  max-width: 900px;
  margin: auto;
  padding: 2rem;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #2f9e44;
  font-size: 0.95rem;
  text-decoration: underline;
}
.back-link:hover {
  text-decoration: none;
}

.tbAdd {
  width: 100%;
  border-top: 1px solid #888;
  border-collapse: collapse;
}
.tbAdd th,
.tbAdd td {
  border-bottom: 1px solid #eee;
  padding: 15px 20px;
  text-align: left;
}
.tbAdd th {
  background: #f9f9f9;
  width: 150px;
}
.tbAdd td.txt_cont {
  height: 300px;
  vertical-align: top;
}

.like-wrapper {
  margin: 1.5rem 0 1rem 0;
}
.like-btn {
  all: unset;
  font-size: 1.3rem;
  cursor: pointer;
}
.like-btn:disabled {
  opacity: 0.5;
  cursor: default;
}

.post-actions {
  float: right;
  margin-left: 10px;
}
.edit-btn,
.delete-btn {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 0.5rem;
}
.edit-btn:hover,
.delete-btn:hover {
  text-decoration: underline;
}

.comment-section {
  margin-top: 2rem;
}
.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.comment-card {
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 0.8rem;
  background-color: #f8f8f8;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.comment-content {
  margin-top: 0.5rem;
}
.comment-date {
  font-size: 0.8rem;
  color: #666;
  text-align: right;
  margin-top: 0.5rem;
}
.comment-delete {
  background: none;
  border: none;
  font-size: 0.8rem;
  color: red;
  cursor: pointer;
}
.comment-form {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-top: 1rem;
}
.comment-form textarea {
  width: 100%;
  padding: 0.5rem;
}
.comment-form button {
  margin-top: 0.5rem;
  padding: 0.4rem 1rem;
  background: #f37075;
  color: white;
  border: none;
  border-radius: 4px;
}
.login-warning {
  color: #999;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>