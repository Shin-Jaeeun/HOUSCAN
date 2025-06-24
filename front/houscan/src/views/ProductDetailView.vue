<template>
  <div class="product-detail-wrapper mt-5 pt-5" v-if="product">
    <div class="product-header-wrapper">
      <RouterLink to="/product" class="back-link">← 목록으로</RouterLink>
      <div class="header-row">
        <div class="bank-logo-box">
          <img :src="getBankImage(product.bank)" class="bank-logo" v-if="product.bank" />
        </div>
        <h2 class="product-title">{{ product.product_name }}</h2>
      </div>
    </div>

    <table class="detail-table">
      <tr><th>금융사</th><td>{{ product.bank }}</td></tr>
      <tr><th>상품명</th><td>{{ product.product_name }}</td></tr>
      <tr><th>6개월 금리</th><td>{{ product.rates['6'] ?? '-' }}%</td></tr>
      <tr><th>12개월 금리</th><td>{{ product.rates['12'] ?? '-' }}%</td></tr>
      <tr><th>24개월 금리</th><td>{{ product.rates['24'] ?? '-' }}%</td></tr>
      <tr><th>36개월 금리</th><td>{{ product.rates['36'] ?? '-' }}%</td></tr>
    </table>

    <a :href="getBankUrl(product.bank)" target="_blank" class="bank-link">
      🔗 공식 사이트로 이동
    </a>

    <div class="favorite-box" v-if="isLoggedIn">
      <button @click="toggleFavorite">
        <span v-if="isFavorite">💔 찜 취소</span>
        <span v-else>❤️ 찜하기</span>
      </button>
    </div>

    <div class="region-selector">
      <select v-model="selectedSido" @change="updateSigungu">
        <option disabled value="">광역시/도 선택</option>
        <option v-for="item in sidoList" :key="item.name" :value="item.name">
          {{ item.name }}
        </option>
      </select>

      <select v-model="selectedSigungu">
        <option disabled value="">시/군/구 선택</option>
        <option v-for="sgg in sigunguList" :key="sgg" :value="sgg">
          {{ sgg }}
        </option>
      </select>

      <button @click="drawMap" class="search-btn">위치 보기</button>
    </div>

    <div class="map-container">
      <h4>근처 {{ product.bank }} 위치</h4>
      <div v-show="!mapDrawn" class="empty-map-placeholder">
        <p class="text-muted mt-2">[위치보기]를 클릭해 주변 은행을 찾아봐요!</p>
        <img :src="MapImage" alt="지도 미리보기" class="placeholder-img" />
      </div>
      <div v-show="mapDrawn" :id="`map-${productId}`" style="width:100%;height:300px;"></div>
    </div>

    <div v-if="searchedBranches.length > 0" class="branch-list mt-4">
      <h5 class="branch-title">📍 근처 {{ product.bank }} 지점</h5>
      <div class="branch-cards">
        <div
          v-for="(branch, index) in searchedBranches"
          :key="index"
          class="branch-card"
          :class="{ selected: selectedBranch && selectedBranch.id === branch.id }"
          @click="selectBranch(branch)"
        >
          <div class="branch-name">{{ branch.place_name }}</div>
          <div class="branch-address">{{ branch.address_name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/useAuthStore'
import mapInfo from '@/assets/data.json'
import MapImage from '@/assets/map.png'

const kakaoKey = import.meta.env.VITE_KAKAO_API_KEY
const route = useRoute()
const productId = parseInt(route.params.id)
const product = ref(null)
const productInstitution = ref('')
const productName = ref('')
const authStore = useAuthStore()
const isLoggedIn = computed(() => authStore.isLogin)
const favoriteId = ref(null)
const isFavorite = computed(() => favoriteId.value !== null)

const sidoList = mapInfo.mapInfo
const selectedSido = ref('')
const selectedSigungu = ref('')
const sigunguList = ref([])

const mapDrawn = ref(false)
const searchedBranches = ref([])
const selectedBranch = ref(null)
const markerMap = new Map()

const updateSigungu = () => {
  const match = sidoList.find(s => s.name === selectedSido.value)
  sigunguList.value = match ? match.countries : []
  selectedSigungu.value = ''
}

const getBankUrl = (name) => {
  const urls = {
    '우리은행': 'https://www.wooribank.com/',
    '부산은행': 'https://www.busanbank.co.kr/',
    '대구은행': 'https://www.dgb.co.kr/',
    '한국스탠다드차타드은행': 'https://www.standardchartered.co.kr/',
    '경남은행': 'https://www.knbank.co.kr/ib20/mnu/BHP000000000001',
    '광주은행': 'https://pib.kjbank.com/ib20/mnu/BPB0000000001',
    '국민은행': 'https://www.kbstar.com/',
    '농협은행주식회사': 'https://www.nhbank.com/nhmn/KO_NHMN_01.do',
    '수협은행': 'https://www.suhyup-bank.com',
    '신한은행': 'https://www.shinhan.com/index.jsp',
    '아이엠뱅크': 'https://www.imbank.co.kr/dgb_ebz_main.jsp',
    '전북은행': 'https://www.jbbank.co.kr/',
    '주식회사 카카오뱅크': 'https://www.kakaobank.com/',
    '주식회사 케이뱅크': 'https://www.kbanknow.com/ib20/mnu/PBKMAN000000',
    '중소기업은행': 'https://www.ibk.co.kr',
    '토스뱅크 주식회사': 'https://www.tossbank.com/',
    '하나은행': 'https://www.kebhana.com/',
    '한국산업은행': 'https://www.kdb.co.kr/index.jsp'
  }
  return urls[name] || '#'
}

const imageMap = import.meta.glob('@/assets/banks/*.png', { eager: true })
const getBankImage = (bank) => {
  const filePath = `/src/assets/banks/${bank}.png`
  const image = imageMap[filePath]
  return image ? image.default : new URL('@/assets/banks/default.png', import.meta.url).href
}

const toggleFavorite = async () => {
  const token = localStorage.getItem('accessToken')
  if (!token) return

  const headers = { headers: { Authorization: `Bearer ${token}` } }
  try {
    if (isFavorite.value) {
      await axios.delete(`http://localhost:8000/api/v1/products/favorites/${favoriteId.value}/`, headers)
      favoriteId.value = null
    } else {
      const res = await axios.post(`http://localhost:8000/api/v1/products/favorites/`, { product_id: productId }, headers)
      favoriteId.value = res.data.id
    }
  } catch (err) {
    const msg = err.response?.data?.non_field_errors?.[0]
    if (msg === '이미 찜한 상품입니다.') isFavorite.value = true
    else if (err.response?.status === 401) alert('로그인이 필요합니다.')
    else alert('찜 처리 중 오류가 발생했습니다.')
  }
}

const loadKakaoScript = () => {
  return new Promise((resolve, reject) => {
    if (window.kakao && window.kakao.maps) return resolve()

    const script = document.createElement('script')
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${kakaoKey}&autoload=false&libraries=services`
    script.onload = () => window.kakao.maps.load(resolve)
    script.onerror = () => reject(new Error('Kakao Map script load error'))
    document.head.appendChild(script)
  })
}

let map, ps, infoWindow
const drawMap = () => {
  const container = document.getElementById(`map-${productId}`)
  if (!container || !product.value?.bank) return

  mapDrawn.value = true
  map = new kakao.maps.Map(container, { center: new kakao.maps.LatLng(37.5665, 126.9780), level: 5 })
  ps = new kakao.maps.services.Places()
  infoWindow = new kakao.maps.InfoWindow({ zIndex: 3 })

  const keyword = `${selectedSido.value} ${selectedSigungu.value} ${product.value.bank}`

  ps.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      searchedBranches.value = data
      const bounds = new kakao.maps.LatLngBounds()
      markerMap.clear()

      data.forEach(place => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        const marker = new kakao.maps.Marker({
          map,
          position,

        })

        markerMap.set(place.id, marker)

        kakao.maps.event.addListener(marker, 'click', () => {
          selectedBranch.value = place
          highlightMarker(place.id)
          infoWindow.setContent(`<div style="padding:6px;font-size:14px;">${place.place_name}<br/>${place.address_name}</div>`)
          infoWindow.open(map, marker)
        })

        bounds.extend(position)
      })

      map.setBounds(bounds)
    } else {
      searchedBranches.value = []
    }
  })
}

const selectBranch = (branch) => {
  selectedBranch.value = branch
  const marker = markerMap.get(branch.id)
  if (marker) {
    map.panTo(new kakao.maps.LatLng(branch.y, branch.x))
    highlightMarker(branch.id)
    infoWindow.setContent(`<div style="padding:6px;font-size:14px;">${branch.place_name}<br/>${branch.address_name}</div>`)
    infoWindow.open(map, marker)
  }
}

const highlightMarker = (targetId) => {
  markerMap.forEach((marker, id) => {
    if (id === targetId) {
      const redImage = new kakao.maps.MarkerImage(
        'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
        new kakao.maps.Size(24, 35)
      )
      marker.setImage(redImage)
    } else {
      // ✅ 기본 파란 마커: 이미지 설정 생략
      marker.setImage(null)
    }
  })
}

onMounted(async () => {
  const token = localStorage.getItem('accessToken')

  try {
    const res1 = await axios.get(`http://localhost:8000/api/v1/products/products/${productId}/`)
    productInstitution.value = res1.data.institution
    productName.value = res1.data.name

    const res2 = await axios.get('http://localhost:8000/api/v1/products/grouped/')
    product.value = res2.data.find(p => p.bank === productInstitution.value && p.product_name === productName.value)
  } catch (err) {
    console.error('❌ 상품 로딩 실패:', err)
    return
  }

  if (token) {
    const headers = { headers: { Authorization: `Bearer ${token}` } }
    try {
      const favRes = await axios.get(`http://localhost:8000/api/v1/products/favorites/`, headers)
      const found = favRes.data.find(fav => fav.product?.id === productId)
      favoriteId.value = found?.id || null
    } catch (err) {
      console.warn('찜 상태 확인 실패:', err)
    }
  }

  await nextTick()
  await loadKakaoScript()
})
</script>


<style scoped>
.product-detail-wrapper {
  padding: 2.5rem;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  max-width: 900px;
  margin: 5rem auto;
  font-family: 'Pretendard', sans-serif;
}

.header-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.bank-logo-box {
  width: 64px;
  height: 64px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f1f3f5;
  border-radius: 8px;
}
.bank-logo {
  height: 40px;
  object-fit: contain;
  max-width: 100%;
}
.product-title {
  font-size: 1.8rem;
  font-weight: 700;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
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
}
.detail-table td {
  color: #495057;
}

.bank-link {
  display: inline-block;
  margin-bottom: 1.5rem;
  color: #2f9e44;
  text-decoration: underline;
  font-weight: 600;
  font-size: 1.1rem;
}

.favorite-box {
  margin-bottom: 2rem;
}
.favorite-box button {
  background-color: #f37075;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 30px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: 0.3s;
}
.favorite-box button:hover {
  background-color: #cc4e56;
}

.region-selector {
  display: flex;
  gap: 1rem;
  margin: 2rem 0 1rem;
  align-items: center;
}
.region-selector select {
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}
.search-btn {
  background-color: #f37075;
  color: white;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.search-btn:hover {
  background-color: #cc4e56;
}

.map-container {
  margin-top: 1rem;
  border: 1px solid #ccc;
  border-radius: 12px;
  overflow: hidden;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.map-container h4 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.product-header-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* ✅ 간격 주는 핵심! */
  margin-bottom: 2rem;
}

.back-link {
  font-size: 1rem;
  color: #2f9e44;
  text-decoration: none;
  display: inline-block;
}

.header-row {
  display: flex;
  align-items: center;
  gap: 1rem; /* ✅ 로고와 제목 간격 */
}

.bank-logo {
  height: 48px;
  width: auto;
}

.empty-map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: #f8f9fa;
  border: 1px dashed #ccc;
  border-radius: 10px;
  color: #888;
}

.placeholder-img {
  width: 150px; /* 또는 200px, 필요에 따라 조절 */
  opacity: 0.6;
  margin-bottom: 0.5rem;
}

.branch-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.branch-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.branch-card {
  padding: 1rem;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  transition: box-shadow 0.2s ease;
}

.branch-card.selected {
  border: 2px solid #2f9e44;
  background-color: #e9fbe9;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.branch-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.branch-name {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.3rem;
  color: black;
}

.branch-address {
  font-size: 0.9rem;
  color: #555;
}


</style>
