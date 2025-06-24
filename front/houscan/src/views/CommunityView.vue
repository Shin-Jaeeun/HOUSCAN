<template>
  <div class="page-wrapper">
    <!-- 🔥 인기글 사이드바 -->
    <div class="community-sidebar-outside">
      <h3>🔥인기글 TOP 5</h3>
      <ul class="popular-posts">
        <li
          v-for="post in topLikedPosts"
          :key="post.id"
          class="popular-post-card"
        >
          <RouterLink :to="{ name: 'CommunityDetail', params: { postId: post.id } }" class="popular-link">
            <p class="popular-title">{{ post.title }}</p>
            <p class="popular-meta">💗 {{ post.like_count || 0 }} | {{ post.user }}</p>
          </RouterLink>
        </li>
      </ul>
    </div>

    <!-- 📋 커뮤니티 본문 -->
    <div class="community-page">
      <h1 class="main-title">커뮤니티</h1>

      <div class="category-tabs">
        <button
          v-for="cat in categories"
          :key="cat"
          :class="{ active: selectedCategory === cat }"
          @click="selectCategory(cat)"
        >
          {{ cat }}
        </button>
      </div>

      <!-- 🔍 검색 + 정렬 + 글쓰기 정렬정돈 -->
      <div class="toolbar">
        <div class="left-controls">
          <input v-model="searchQuery" type="text" placeholder="제목 검색" />
          <select id="sortSelect" v-model="sortOption">
            <option value="latest">최신순</option>
            <option value="popular">인기순</option>
          </select>
        </div>
        <RouterLink v-if="isLogin" to="/community/create" class="write-btn">
          ✏️ 글쓰기
        </RouterLink>
      </div>


      <p class="post-count">총 {{ filteredPosts.length }}개의 게시글이 있습니다.</p>

      <table class="post-table">
        <thead>
          <tr>
            <th>No</th>
            <th>카테고리</th>
            <th>제목</th>
            <th>작성자</th>
            <th>좋아요</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(post, index) in paginatedPosts" :key="post.id">
            <td>{{ index + 1 + (currentPage - 1) * postsPerPage }}</td>
            <td>{{ post.category }}</td>
            <td>
              <RouterLink :to="{ name: 'CommunityDetail', params: { postId: post.id } }" class="title-link">
                {{ post.title }}
              </RouterLink>
            </td>
            <td>{{ post.user }}</td>
            <td><span :class="{ liked: post.is_liked }">💗</span> {{ post.like_count || 0 }}</td>
          </tr>
        </tbody>
      </table>

      <div class="pagination">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page"
          :class="{ active: currentPage === page }"
        >
          {{ page }}
        </button>
      </div>

      <div class="mine-filter-below">
        <label>
          <input type="checkbox" v-model="onlyMine" />
          내가 쓴 글만 보기
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const authStore = useAuthStore()
const isLogin = computed(() => authStore.isLogin)
const username = computed(() => authStore.username)

const categories = ['전체', '아파트', '임의공급', '주택', '토지', '상가', '예적금', '자유게시판']
const selectedCategory = ref('전체')
const searchQuery = ref('')
const sortOption = ref('latest')
const onlyMine = ref(false)
const posts = ref([])

const currentPage = ref(1)
const postsPerPage = 10

const fetchPosts = async () => {
  const res = await axios.get('http://localhost:8000/api/v1/community/posts/')
  posts.value = res.data
}

onMounted(fetchPosts)

const selectCategory = (cat) => {
  selectedCategory.value = cat
  currentPage.value = 1
}

const filteredPosts = computed(() => {
  let result = posts.value
    .filter(post => selectedCategory.value === '전체' || post.category === selectedCategory.value)
    .filter(post => post.title.toLowerCase().includes(searchQuery.value.toLowerCase()))
    .filter(post => !onlyMine.value || post.user === username.value)

  if (sortOption.value === 'latest') {
    result = result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else if (sortOption.value === 'popular') {
    result = result.sort((a, b) => (b.like_count || 0) - (a.like_count || 0))
  }

  return result
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage
  return filteredPosts.value.slice(start, start + postsPerPage)
})

const totalPages = computed(() => {
  return Math.ceil(filteredPosts.value.length / postsPerPage)
})

const topLikedPosts = computed(() => {
  return [...posts.value]
    .sort((a, b) => (b.like_count || 0) - (a.like_count || 0))
    .slice(0, 5)
})
</script>

<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;
  gap: 2rem;
  padding: 2rem;
}

.community-page {
  flex: 1;
  max-width: 900px;
}

.community-sidebar-outside {
  width: 250px;
  position: sticky;
  top: 120px;
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  height: fit-content;
}

.community-sidebar-outside > h3{
  color: black;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
}
.popular-posts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popular-post-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 1rem;
  transition: box-shadow 0.2s;
}

.popular-post-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.popular-link {
  text-decoration: none;
  color: inherit;
}

.popular-title {
  font-weight: bold;
  font-size: 1rem;
  margin: 0 0 0.3rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.popular-meta {
  font-size: 0.85rem;
  color: #666;
}

.main-title {
  font-size: 2.3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
}

.write-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.7rem;
}

.write-btn {
  font-size: 0.95rem;
  color: #2f9e44;
  text-decoration: none;
  padding: 0.4rem 0.8rem;
  border: 1px solid #2f9e44;
  border-radius: 4px;
  transition: background 0.2s;
}

.write-btn:hover {
  background: #e6f4ea;
}

.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #ccc;
  border-top: 2px solid #ccc;
}

.category-tabs button {
  background: none;
  border: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  padding: 0.3rem 0.7rem;
  border-bottom: 2px solid transparent;
}

.category-tabs button.active {
  color: #2f9e44;
  font-weight: bold;

}

.filter-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.5rem;
}

.filter-bar input {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 300px;
}

.mine-filter-below {
  margin-top: 0.5rem;
  text-align: left;
  font-size: 0.9rem;
  color: #555;
}

.post-count {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 0.5rem;
  text-align: left;
}

.post-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.post-table thead {
  background: #f9f9f9;
  border-top: 2px solid #ccc;
}

.post-table th,
.post-table td {
  padding: 0.75rem;
  border-top: 1px solid #ddd;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.post-table td:nth-child(3) {
  text-align: left;
}

.title-link {
  color: #333;
  text-decoration: none;
}

.title-link:hover {
  text-decoration: underline;
  color: #2f9e44;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.pagination button {
  padding: 0.4rem 0.8rem;
  border: 1px solid #ccc;
  background: white;
  color: #333;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button.active {
  background: #2f9e44;
  color: white;
  border-color: #2f9e44;
}

.liked {
  color: #e64980;
  font-weight: bold;
}

.sort-bar {
  display: none;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.left-controls {
  display: flex;
  gap: 0.5rem;
}

.left-controls input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 200px;
}

.left-controls select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.write-btn {
  font-size: 0.95rem;
  color: #2f9e44;
  text-decoration: none;
  padding: 0.4rem 0.8rem;
  border: 1px solid #2f9e44;
  border-radius: 4px;
  transition: background 0.2s;
}

.write-btn:hover {
  background: #e6f4ea;
}

</style>