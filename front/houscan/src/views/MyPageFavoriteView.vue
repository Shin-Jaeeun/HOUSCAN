<template>
  <div class="mypage-favorite container py-5 mt-5 pt-5">
    <!-- 예적금 영역 -->
    <section class="favorite-section deposit-section">
      <h2 class="section-title">찜한 예적금 상품</h2>
      <div v-if="depositFavorites.length > 0" class="card-list">
        <div v-for="fav in depositFavorites" :key="fav.id" class="card product-card">
          <div class="card-body">
            <h5 class="card-title">{{ fav.product.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ fav.product.institution }}</h6>
            <p class="card-text">금리: <strong>{{ fav.product.option_base_rate }}%</strong></p>
            <div class="btn-group">
              <RouterLink :to="`/product/${fav.product.id}`" class="btn btn-success btn-sm">상세보기</RouterLink>
              <button class="btn btn-outline-danger btn-sm" @click="removeDepositFavorite(fav.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>
      <p v-else class="empty-text">아직 찜한 예적금 상품이 없습니다.</p>
    </section>

    <!-- 청약 공고 영역 -->
    <section class="favorite-section notice-section">
      <h2 class="section-title">찜한 청약 공고</h2>
      <div v-if="noticeFavorites.length > 0" class="card-list">
        <div v-for="fav in noticeFavorites" :key="fav.id" class="card notice-card">
          <img v-if="fav.notice.image_url" :src="fav.notice.image_url" alt="청약 공고 이미지" class="card-img-top" />
          <div class="card-body">
            <div v-if="fav.notice.apply_end" class="deadline-badge"
              :class="{ 'warning': daysLeft(fav.notice.apply_end) <= 3 && daysLeft(fav.notice.apply_end) >= 0 }">
              D-{{ daysLeft(fav.notice.apply_end) }}
            </div>
            <h5 class="card-title">{{ fav.notice.title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ fav.notice.category }} / {{ fav.notice.location }}</h6>
            <div class="btn-group">
              <RouterLink :to="`/houselist/${fav.notice.id}`" class="btn btn-success btn-sm">상세보기</RouterLink>
              <button class="btn btn-outline-danger btn-sm" @click="removeNoticeFavorite(fav.id)">삭제</button>
            </div>
          </div>
        </div>
      </div>
      <p v-else class="empty-text">아직 찜한 청약 공고가 없습니다.</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'


// 남은 일수를 계산하는 함수 (apply_end를 YYYY-MM-DD 형식으로 가정)
function daysLeft(apply_end) {
  if (!apply_end) return -1
  const today = new Date()
  const endDate = new Date(apply_end)
  const diffTime = endDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays >= 0 ? diffDays : 0
}

const depositFavorites = ref([])
const noticeFavorites = ref([])

const token = localStorage.getItem('accessToken')
const headers = { headers: { Authorization: `Bearer ${token}` } }

onMounted(async () => {
  try {
    const res1 = await axios.get('http://localhost:8000/api/v1/products/favorites/', headers)
    depositFavorites.value = res1.data

    const res2 = await axios.get('http://localhost:8000/api/v1/houses/favorites/', headers)
    noticeFavorites.value = res2.data
  } catch (err) {
    console.error('찜 목록 조회 실패:', err)
  }
})

const removeDepositFavorite = async (favoriteId) => {
  try {
    await axios.delete(`http://localhost:8000/api/v1/products/favorites/${favoriteId}/`, headers)
    depositFavorites.value = depositFavorites.value.filter(f => f.id !== favoriteId)
    // alert('예적금 찜 삭제 완료')
  } catch (err) {
    console.error('삭제 실패:', err)
    // alert('예적금 삭제 중 오류 발생')
  }
}

const removeNoticeFavorite = async (favoriteId) => {
  try {
    await axios.delete(`http://localhost:8000/api/v1/houses/favorites/${favoriteId}/`, headers)
    noticeFavorites.value = noticeFavorites.value.filter(f => f.id !== favoriteId)
    // alert('청약 찜 삭제 완료')
  } catch (err) {
    console.error('삭제 실패:', err)
    // alert('청약 삭제 중 오류 발생')
  }
}
</script>

<style scoped>
.mypage-favorite {
  font-family: 'Pretendard', sans-serif;
  padding: 4rem 1rem 2rem;
  min-height: 100vh;
}

.favorite-section {
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 3rem;
  box-shadow: 0 4px 15px rgb(0 0 0 / 0.1);
  background-color: white;
}

.deposit-section {
  /* 예적금 배경은 기본 흰색 */
}

.notice-section {
  background-color: #f0f7f7;
}

.section-title {
  color: black;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

.card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.product-card,
.notice-card {
  flex: 1 1 calc(33% - 1rem);
  max-width: 320px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgb(0 0 0 / 0.08);
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
}

.product-card:hover,
.notice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgb(0 0 0 / 0.15);
}

.notice-card img {
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  height: 180px;
  width: 100%;
  object-fit: cover;
}

.deadline-badge {
  background-color: #2F9E44;
  color: white;
  font-weight: 700;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.deadline-badge.warning {
  background-color: #d32f2f;
}

.card-title {
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.85rem;
  color: #757575;
  margin-bottom: 1rem;
}

.card-text {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.btn-group {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
}

.btn-success {
  background-color: #f37075;
  border-color: #f37075;
  font-size: 0.85rem;
  padding: 0.35rem 0.7rem;
  border-radius: 8px;
  font-weight: 600;
}

.btn-success:hover {
  background-color: #fce9ed;
  border-color: #fce9ed;
}

.btn-outline-danger {
  color: #d32f2f;
  border-color: transparent;
  background: none;
  font-size: 0.85rem;
  padding: 0.35rem 0.7rem;
  border-radius: 8px;
  font-weight: 600;
  transition: background-color 0.25s ease, color 0.25s ease;
}

.btn-outline-danger:hover {
  background-color: #d32f2f;
  color: white;
  border-color: #d32f2f;
  box-shadow: 0 0 6px rgba(211, 47, 47, 0.5);
  cursor: pointer;
}

.empty-text {
  font-style: italic;
  color: #999;
  margin-top: 1rem;
  text-align: center;
}

/* 반응형 */
@media (max-width: 992px) {

  .product-card,
  .notice-card {
    flex: 1 1 calc(50% - 1rem);
  }
}

@media (max-width: 576px) {

  .product-card,
  .notice-card {
    flex: 1 1 100%;
  }
}
</style>
