<template>
  <div class="notice-detail" v-if="notice">
    <RouterLink to="/houselist" class="back-link">← 목록으로</RouterLink>
    <div class="header-row">
      <img :src="notice.image_url" v-if="notice.image_url" class="notice-thumbnail" />
      <h2 class="notice-title fw-bold">{{ notice.title }}</h2>
    </div>

    <table class="detail-table">
      <tr><th>카테고리</th><td>{{ notice.category }}</td></tr>
      <tr><th>접수 기간</th><td>{{ notice.apply_start }} ~ {{ notice.apply_end }}</td></tr>
      <tr><th>공급 위치</th><td>{{ notice.location || '정보 없음' }}</td></tr>
      <tr><th>공급 규모</th><td>{{ notice.scale || '정보 없음' }}</td></tr>
      <tr><th>당첨자 발표일</th><td>{{ notice.winner_announcement_date || '정보 없음' }}</td></tr>
    </table>


    <p v-if="notice.notice_url" class="notice-file-link">
      <a :href="notice.notice_url" target="_blank" class="notice-link">
        <img src="@/assets/file.png" alt="첨부파일" class="file-icon" /> 모집공고문 첨부파일
      </a>
    </p>
    <p v-if="notice.detail_url" class="notice-detail-link">
      <a :href="notice.detail_url" target="_blank" class="detail-link">
        <img src="@/assets/link.png" alt="링크 아이콘" class="link-icon" /> 더 자세한 정보 보기
      </a>
    </p>

    <!-- ✅ 로그인한 경우에만 찜 버튼 보이도록 수정 -->
    <div class="favorite-box" v-if="authStore.isLogin">
      <button @click="toggleFavorite" :disabled="isLoading">
        <span v-if="isFavorited">💔 찜 취소</span>
        <span v-else>❤️ 찜하기</span>
      </button>
      <span>총 {{ notice.favorites_count ?? 0 }}명 찜</span>
    </div>


    <div id="map"></div>

    <div v-if="nearbyPlaces.length > 0" class="nearby-section">
      <p v-if="nearestStation" class="fs-5">
        📍 가장 가까운 역: <strong>{{ nearestStation.name }}</strong>
        (도보 약 <strong>{{ nearestStation.minutes }}분</strong>)
      </p>
      <hr />
      <h4 class="fs-5 fw-semibold">📍 주변 편의시설</h4>
      <ul class="nearby-list">
        <li v-for="place in nearbyPlaces" :key="place.id">
          {{ place.place_name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/useAuthStore'

const route = useRoute()
const authStore = useAuthStore()
const notice = ref(null)
const isFavorited = ref(false)
const favoriteId = ref(null)
const isLoading = ref(false)
const nearestStation = ref(null)
const nearbyPlaces = ref([])
const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_API_KEY

const loadKakaoMap = async () => {
  if (!notice.value.location) return
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false&libraries=services`
  document.head.appendChild(script)

  script.onload = () => {
    kakao.maps.load(() => {
      const mapContainer = document.getElementById('map')
      const map = new kakao.maps.Map(mapContainer, {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 3
      })
      const geocoder = new kakao.maps.services.Geocoder()

      geocoder.addressSearch(notice.value.location, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
          const coords = new kakao.maps.LatLng(result[0].y, result[0].x)
          new kakao.maps.Marker({ map, position: coords })
          map.setCenter(coords)
          findNearestStation(coords)
          findNearbyPlaces(coords)
        }
      })
    })
  }
}

function findNearbyPlaces(coords) {
  const ps = new kakao.maps.services.Places()
  ps.keywordSearch('편의점', (data, status) => {
    if (status === kakao.maps.services.Status.OK && data.length > 0) {
      nearbyPlaces.value = data.slice(0, 5)
    }
  }, {
    location: coords,
    radius: 1000
  })
}

function getDistanceFromLatLonInMeters(lat1, lon1, lat2, lon2) {
  const R = 6371e3
  const φ1 = lat1 * Math.PI / 180
  const φ2 = lat2 * Math.PI / 180
  const Δφ = (lat2 - lat1) * Math.PI / 180
  const Δλ = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const findNearestStation = (coords) => {
  const ps = new kakao.maps.services.Places()
  ps.keywordSearch('지하철역', (data, status) => {
    if (status === kakao.maps.services.Status.OK && data.length > 0) {
      const sorted = data.map(place => {
        const dist = getDistanceFromLatLonInMeters(
          coords.getLat(), coords.getLng(),
          parseFloat(place.y), parseFloat(place.x)
        )
        return { ...place, dist }
      }).sort((a, b) => a.dist - b.dist)
      const nearest = sorted[0]
      const minutes = Math.round(nearest.dist / 67) || 1
      nearestStation.value = {
        name: nearest.place_name,
        minutes
      }
    }
  }, {
    location: coords,
    radius: 2000
  })
}

const fetchNotice = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/api/v1/houses/houselist/${route.params.id}/`)
    notice.value = res.data
    await checkIfFavorited()
    await nextTick()
    await loadKakaoMap()
  } catch (err) {
    console.error('❌ 공고 상세 불러오기 실패:', err)
  }
}

const checkIfFavorited = async () => {
  const token = localStorage.getItem('accessToken')
  const headers = { headers: { Authorization: `Bearer ${token}` } }
  try {
    const res = await axios.get('http://localhost:8000/api/v1/houses/favorites/', headers)
    const match = res.data.find(fav => fav.notice.id === Number(route.params.id))
    if (match) {
      isFavorited.value = true
      favoriteId.value = match.id
    } else {
      isFavorited.value = false
      favoriteId.value = null
    }
  } catch (err) {
    console.error('❌ 찜 여부 확인 실패:', err)
  }
}

const toggleFavorite = async () => {
  const token = localStorage.getItem('accessToken')
  const headers = { headers: { Authorization: `Bearer ${token}` } }
  try {
    if (isFavorited.value && favoriteId.value) {
      await axios.delete(`http://localhost:8000/api/v1/houses/favorites/${favoriteId.value}/`, headers)
      isFavorited.value = false
      favoriteId.value = null
      notice.value.favorites_count = Math.max((notice.value.favorites_count ?? 1) - 1, 0)
    } else {
      const res = await axios.post('http://localhost:8000/api/v1/houses/favorites/', {
        notice: route.params.id
      }, headers)
      isFavorited.value = true
      favoriteId.value = res.data.id
      notice.value.favorites_count = (notice.value.favorites_count ?? 0) + 1
    }
  } catch (err) {
    alert('찜 처리 중 오류 발생')
  }
}

onMounted(fetchNotice)
</script>

<style scoped>
.notice-detail {
  max-width: 1200px;
  min-height: 60vh;
  margin: 6rem auto 2rem;
  padding: 2.5rem;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.header-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.notice-thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  background: #e9ecef;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}
.detail-table th,
.detail-table td {
  padding: 0.75rem 1.2rem;
  border: 1px solid #dee2e6;
  vertical-align: middle;
}
.detail-table th {
  background-color: #f8f9fa;
  width: 180px;
  color: #343a40;
  text-align: left;
  white-space: nowrap;
}
.detail-table td {
  color: #495057;
}

.favorite-box {
  margin-top: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.05rem;
}
.favorite-box button {
  background-color: #ff6b81;
  border: none;
  color: white;
  padding: 0.5rem 1.2rem;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.favorite-box button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.favorite-box button:hover {
  background-color: #cc4e56;
}

#map {
  width: 100%;
  height: 360px;
  margin-top: 4rem;
  border-radius: 10px;
  overflow: hidden;
}

.nearby-section {
  margin-top: 2rem;
  background: #f8f9fa;
  padding: 1rem 1.5rem;
  border-radius: 10px;
}
.nearby-section h4 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #343a40;
}
.nearby-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.nearby-list li {
  font-size: 1.05rem;
  padding: 0.3rem 0;
  color: #495057;
}

.notice-file-link,
.notice-detail-link {
  margin-top: 1rem;
}
.notice-link,
.detail-link {
  color: #1971c2;
  font-weight: bold;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.notice-link:hover,
.detail-link:hover {
  color: #0b5ed7;
  text-decoration: underline;
}
.file-icon,
.link-icon {
  width: 30px;
  height: 30px;
}

.back-link {
  display: inline-block;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  color: #2f9e44;
  text-decoration: none;
  font-weight: 500;
}

.back-link:hover {
  color: #2f9e44;
  text-decoration: underline;
}
</style>