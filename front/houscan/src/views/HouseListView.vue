<template>
  <div class="house-page pt-5 mt-5" style="padding-top: 7rem;">
    <!-- 🔹 왼쪽: 공고 리스트 -->
    <div class="house-list">
      <h1 class="main-title">청약 공고 리스트</h1>

      <!-- 🔹 필터 영역 -->
      <div class="filter-group">
        <div class="filter-tabs">
          <span>카테고리:</span>
          <button v-for="cat in categoryOptions" :key="cat" @click="selectedCategory = cat"
            :class="{ active: selectedCategory === cat }">
            {{ cat }}
          </button>
        </div>
        <div class="filter-tabs">
          <span>상태:</span>
          <button v-for="status in statusOptions" :key="status" @click="selectedStatus = status"
            :class="{ active: selectedStatus === status }">
            {{ status }}
          </button>
        </div>
        <div class="sort-box">
          <label for="sort">정렬:</label>
          <select id="sort" v-model="sortOption">
            <option value="favorites">인기순</option>
            <option value="deadline">마감 임박순</option>
          </select>
        </div>
      </div>

      <!-- 🔹 리스트 테이블 -->
      <table class="notice-table">
        <thead>
          <tr>
            <th></th>
            <th >이름</th>
            <th>카테고리</th>
            <th>시작일</th>
            <th>마감일</th>
            <th>상태</th>
            <th>찜</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="notice in sortedNotices"
            :key="notice.id"
            class="clickable-row"
            @click="goToDetail(notice.id)"
          >
            <td><img :src="notice.image_url || defaultImage" class="mini-thumb" /></td>
            <td><div class="ellipsis-text fs-5">{{ notice.title }}</div></td>
            <td>{{ notice.category }}</td>
            <td>{{ notice.apply_start }}</td>
            <td>{{ notice.apply_end }}</td>
            <td>
              <span :class="['status-badge', notice.status === '접수중' ? 'active' : 'waiting']">
                {{ notice.status }}
              </span>
            </td>
            <td class="favorite-cell">❤️ {{ notice.favorites_count ?? 0 }}</td>
            <td></td> <!-- 자세히 버튼 제거 -->
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 🔹 오른쪽: 찜 많은 공고 -->
    <div class="sidebar">
      <h2>🔥 찜 많은 공고</h2>
      <div v-for="item in topFavorites" :key="item.id" class="favorite-card">
        <img :src="item.image_url || defaultImage" alt="썸네일" class="thumbnail" />
        <div class="info">
          <RouterLink :to="`/houselist/${item.id}`" class="title">{{ item.title }}</RouterLink>
          <p class="category">{{ item.category }}</p>
          <p class="period">{{ item.apply_start }} ~ {{ item.apply_end }}</p>
          <p class="likes">❤️ {{ item.favorites_count ?? 0 }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const goToDetail = (id) => {
  router.push(`/houselist/${id}`)
}

const notices = ref([])
const selectedCategory = ref('전체')
const selectedStatus = ref('전체')
const sortOption = ref('deadline')

const categoryOptions = ['전체', '아파트', '임의공급', '분양주택', '임대주택', '토지', '상가']
const statusOptions = ['전체', '접수중', '당첨대기']

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/v1/houses/houselist/')
    notices.value = res.data
  } catch (err) {
    console.error('❌ 공고 리스트 로딩 실패:', err)
  }
})

const filteredNotices = computed(() => {
  let filtered = [...notices.value]
  if (selectedCategory.value !== '전체') {
    filtered = filtered.filter(n => n.category === selectedCategory.value)
  }
  if (selectedStatus.value !== '전체') {
    filtered = filtered.filter(n => n.status === selectedStatus.value)
  }
  return filtered
})

const sortedNotices = computed(() => {
  const sorted = [...filteredNotices.value]
  if (sortOption.value === 'deadline') {
    sorted.sort((a, b) => new Date(a.apply_end) - new Date(b.apply_end))
  } else if (sortOption.value === 'favorites') {
    sorted.sort((a, b) => (b.favorites_count ?? 0) - (a.favorites_count ?? 0))
  }
  return sorted
})

const topFavorites = computed(() => {
  return [...notices.value]
    .sort((a, b) => (b.favorites_count ?? 0) - (a.favorites_count ?? 0))
    .slice(0, 5)
})

const defaultImage = '/default-thumbnail.jpg'
</script>


<style scoped>

.main-title {
  font-size: 3rem;
  font-family: 'Pretendard', sans-serif;
  font-weight: 800;
  border-bottom: 3px solid #e0e0e0;
  padding-bottom: 0.5rem;
  margin-bottom: 2rem;
}

.house-page {
  display: flex;
  gap: 2rem;
  max-width: 1600px;
  margin: 3rem auto;
  padding: 0 2rem;
}

.house-list {
  flex: 3;
}

.sidebar {
  position: sticky;
  top: 7rem;
  flex: 1.8; /* 🔥 비율을 더 키워서 더 많은 공간을 확보 */
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  height: fit-content;
  min-width: 360px;     /* ✅ 최소 너비 확대 */
  max-width: 600px;     /* ✅ 최대 너비도 늘려서 확실한 공간 확보 */
}

.sidebar h2 {
  font-size: 1.3rem;
  margin-bottom: 1.2rem;
  font-weight: bold;
  color: #343a40;
}

.favorite-card {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.thumbnail {
  width: 90px;
  height: 90px;
  object-fit: cover;
  border-radius: 6px;
  background-color: #dee2e6;
}

.info .title {
  font-weight: bold;
  font-size: 1.05rem;
  color: #1971c2;
  text-decoration: none;
  display: block;
  margin-bottom: 0.3rem;
  line-height: 1.3;
}

.info .title:hover {
  text-decoration: underline;
}

.category,
.period,
.likes {
  font-size: 0.95rem;
  color: #495057;
  margin: 0.15rem 0;
}

.notice-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1.15rem;
  table-layout: auto;
}

.notice-table th,
.notice-table td {
  padding: 1.2rem;
  border-bottom: 1px solid #dee2e6;
  text-align: left;
  vertical-align: middle;
  /* white-space: nowrap; */
}

.notice-table th {
  background-color: #f1f3f5;
  color: #343a40;
  font-size: 1.05rem;
}

.notice-table tr:hover {
  background-color: #f8f9fa;
}

.notice-table th:nth-child(1),
.notice-table td:nth-child(1) {
  width: 80px;
  text-align: center;
}

.notice-table th:nth-child(2),
.notice-table td:nth-child(2) {
  width: 35%;
}

.notice-table th:nth-child(3),
.notice-table td:nth-child(3) {
  width: 10%;
  white-space: nowrap;
}

.notice-table th:nth-child(4),
.notice-table td:nth-child(4),
.notice-table th:nth-child(5),
.notice-table td:nth-child(5),
.notice-table th:nth-child(6),
.notice-table td:nth-child(6) {
  width: 110px;
  white-space: nowrap;
}

.notice-table th:nth-child(7),
.notice-table td:nth-child(7) {
  width: 60px;
  text-align: center;
}

.notice-table th:nth-child(8),
.notice-table td:nth-child(8) {
  width: 80px;
  text-align: center;
}

.title-with-thumb {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  line-height: 1.4;
  white-space: normal;
  overflow: hidden;
}

.mini-thumb {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
  background-color: #dee2e6;
  display: block;
  margin: 0 auto;
}


.filter-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-tabs,
.sort-box {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-tabs span,
.sort-box label {
  font-weight: bold;
  font-size: 1.1rem;
}

.filter-tabs button {
  padding: 0.5rem 1rem;
  border: 1px solid #ced4da;
  background-color: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1.05rem;
  transition: 0.2s;
}

.filter-tabs button.active {
  background-color: #f37075;
  color: white;
  font-weight: bold;
  border-color: #f37075;
}

.sort-box select {
  padding: 0.5rem 1rem;
  font-size: 1.05rem;
  border: 1px solid #ced4da;
  border-radius: 6px;
}

.detail-link {
  color: #1971c2;
  font-weight: bold;
  text-decoration: none;
  white-space: nowrap;
}

.detail-link:hover {
  text-decoration: underline;
}

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 1.5rem;
  font-size: 1.05rem;
  font-weight: bold;
  white-space: nowrap;
  min-width: 90px;
  text-align: center;
}

.status-badge.active {
  background-color: #d3f9d8;
  color: #2b8a3e;
}

.status-badge.waiting {
  background-color: #fff3bf;
  color: #f59f00;
}

.ellipsis-text {
  display: block;
  font-weight: 500;
  font-size: 1rem;
  line-height: 1.3;
  margin: 0;
  padding: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.favorite-cell {
  text-align: center;
  white-space: nowrap;
  font-size: 1.05rem;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.clickable-row:hover {
  background-color: #f1f3f5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
</style>
