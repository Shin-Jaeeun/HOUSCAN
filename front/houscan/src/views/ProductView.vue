<template>
  <div class="product-wrapper container mt-5 pt-5">
    <!-- 목표자산 설정 폼 -->
    <h2 class="main-title text-center">예적금 상품 추천</h2>
    <div class="top-form card p-4 mb-4">
      <div class="row g-3 align-items-end">
        <div class="col-md-4">
          <label class="form-label">목표 자산 (만원)</label>
          <input v-model.number="inputGoalAsset" type="number" class="form-control" />
        </div>
        <div class="col-md-4">
          <label class="form-label">목표 도달 시점</label>
          <input v-model="inputTargetDate" type="date" class="form-control" />
        </div>
        <div class="col-md-4">
          <label class="form-label">예치금 / 매월 납입금 (만원)</label>
          <input v-model.number="inputMonthlyPayment" type="number" class="form-control" />
        </div>
        <div class="col-12 mt-3 d-flex gap-3">
          <button class="recommend-btn w-100" @click="applyRecommendation">
            추천 상품 보기
          </button>
          <button class="btn btn-outline-secondary w-100" @click="resetRecommendation">
            모든 상품 보기
          </button>
        </div>
      </div>
    </div>

    <!-- 은행 카드 -->
    <div id="bankCarousel" class="carousel slide mb-4" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div
          v-for="(chunk, index) in bankChunks"
          :key="index"
          class="carousel-item"
          :class="{ active: index === 0 }"
        >
          <div class="container">
            <div class="row row-cols-5 g-3">
              <div
                v-for="bank in chunk"
                :key="bank"
                class="col text-center bank-card"
                :class="{ active: bank === selectedBank }"
                @click="selectBank(bank)"
              >
                <img :src="getBankImage(bank)" class="img-fluid" style="height: 40px" />
                <p class="mt-2">{{ bank }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button class="carousel-control-prev" type="button" data-bs-target="#bankCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon"></span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#bankCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon"></span>
      </button>
    </div>

    <hr class="divider my-5" />

    <!-- 상품 테이블 -->
    <div v-if="selectedBank">
      <h4>{{ selectedBank }}의 {{ selectedType }} 상품</h4>
      <div class="tabs my-3">
        <button :class="{ active: selectedType === '예금' }" @click="selectedType = '예금'">예금</button>
        <button :class="{ active: selectedType === '적금' }" @click="selectedType = '적금'">적금</button>
      </div>

      <table class="product-table">
        <thead>
          <tr>
            <th>상품명</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>24개월</th>
            <th>36개월</th>
            <th v-if="isRecommended">추천 설명</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProductsByBank" :key="product.name">
            <td>
              <RouterLink :to="`/product/${product.id}`" class="link">{{ product.name }}</RouterLink>
            </td>
            <td>{{ product.rates?.[6] ?? '-' }}%</td>
            <td>{{ product.rates?.[12] ?? '-' }}%</td>
            <td>{{ product.rates?.[24] ?? '-' }}%</td>
            <td>{{ product.rates?.[36] ?? '-' }}%</td>
            <td v-if="isRecommended" class="recommend-text">{{ product.recommended_message }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 모아보기 버튼 -->
    <div class="text-center my-5">
      <button class="custom-modal-btn me-5" @click="openModal('예금')">모든 은행 예금 모아보기</button>
      <button class="custom-modal-btn" @click="openModal('적금')">모든 은행 적금 모아보기</button>
    </div>

    <!-- 모달 -->
    <ProductModal
      v-if="showModal"
      :type="modalType"
      :products="filteredProductsByType"
      :showRecommend="isRecommended"
      @close="showModal = false"
    />
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import dayjs from 'dayjs'
import ProductModal from '@/views/ProductModal.vue'

const productsRaw = ref([])
const products = ref([])

const selectedBank = ref(null)
const selectedType = ref('예금')

const inputGoalAsset = ref()
const inputTargetDate = ref(dayjs().format('YYYY-MM-DD'))
const inputMonthlyPayment = ref()

const goalAsset = ref()
const targetDate = ref()
const monthlyPayment = ref()

const isRecommended = ref(false)
const showModal = ref(false)
const modalType = ref('예금')

const applyRecommendation = () => {
  goalAsset.value = inputGoalAsset.value
  targetDate.value = inputTargetDate.value
  monthlyPayment.value = inputMonthlyPayment.value
  isRecommended.value = true
}
const resetRecommendation = () => {
  isRecommended.value = false
}

const toggleRecommend = () => isRecommended.value = !isRecommended.value
const selectBank = (bank) => {
  selectedBank.value = selectedBank.value === bank ? null : bank
}
const recommendBtnText = computed(() => isRecommended.value ? '모든 상품 보기' : '추천 상품 받기')

const openModal = (type) => {
  modalType.value = type
  showModal.value = true
}

const imageMap = import.meta.glob('@/assets/banks/*.png', { eager: true })

// 2. 파일 이름 매핑용 함수
const getBankImage = (bank) => {
  const filePath = `/src/assets/banks/${bank}.png`
  const image = imageMap[filePath]
  if (image) {
    // console.log(`✅ 실제 존재함: ${filePath}`)
    return image.default
  } else {
    // console.warn(`❌ 실제 없음: ${filePath}`)
    return new URL('@/assets/banks/default.png', import.meta.url).href
  }
}
const uniqueBanks = computed(() => [...new Set(products.value.map(p => p.institution))])

// ✅ 추천모드 시 그룹핑 + rates 누적
const groupedRecommended = computed(() => {
  const totalMonths = dayjs(targetDate.value).diff(dayjs(), 'month')
  const targetAmount = goalAsset.value * 10000
  const monthly = monthlyPayment.value * 10000
  const grouped = { '예금': [], '적금': [] }
  const groupedMap = {}

  productsRaw.value.forEach(p => {
    const n = parseInt(p.option_saving_period)
    if (!n || isNaN(n)) return

    const key = p.institution + '::' + p.name
    if (!groupedMap[key]) {
      groupedMap[key] = {
        id: p.id,
        name: p.name,
        institution: p.institution,
        preferred_type: p.preferred_type,
        option_base_rate: p.option_base_rate,
        option_max_rate: p.option_max_rate,
        rates: {},
      }
    }

    // 금리 누적
    groupedMap[key].rates[n] = p.option_base_rate

    // 추천 조건 계산
    const r = (p.option_base_rate || 0) / 100
    const finalAmount = p.preferred_type === '예금'
      ? monthly * (1 + r * n / 12)
      : monthly * n * (1 + r * (n + 1) / 24)

    if (finalAmount >= targetAmount * 0.9) {
      groupedMap[key].recommended_message = p.preferred_type === '예금'
        ? `${monthlyPayment.value}만원 예치 → 약 ${Math.floor(finalAmount / 10000)}만원 수령 예상`
        : `매월 ${monthlyPayment.value}만원씩 ${n}개월 납입 → 약 ${Math.floor(finalAmount / 10000)}만원 예상`
    }
  })

  Object.values(groupedMap).forEach(item => {
    if (item.recommended_message) {
      grouped[item.preferred_type].push(item)
    }
  })

  return grouped
})

const bankChunks = computed(() => {
  const all = [...new Set(products.value.map(p => p.institution))]
  const chunks = []
  for (let i = 0; i < all.length; i += 10) {
    chunks.push(all.slice(i, i + 10))
  }
  return chunks
})

// ✅ 전체 상품 통합 (추천모드 아닐 때도 rates 누적)
const buildFullProducts = (raw) => {
  const map = {}
  raw.forEach(p => {
    const n = parseInt(p.option_saving_period)
    if (!n || isNaN(n)) return

    const key = p.institution + '::' + p.name
    if (!map[key]) {
      map[key] = {
        id: p.id,
        name: p.name,
        institution: p.institution,
        preferred_type: p.preferred_type,
        option_base_rate: p.option_base_rate,
        option_max_rate: p.option_max_rate,
        rates: {},
      }
    }

    map[key].rates[n] = p.option_base_rate
  })

  return Object.values(map)
}

const filteredProductsByBank = computed(() => {
  if (!selectedBank.value) return []

  if (isRecommended.value) {
    return (groupedRecommended.value[selectedType.value] || []).filter(
      p => p.institution === selectedBank.value
    )
  } else {
    return products.value.filter(
      p => p.institution === selectedBank.value && p.preferred_type === selectedType.value
    )
  }
})

const filteredProductsByType = computed(() => {
  return isRecommended.value
    ? groupedRecommended.value[modalType.value]
    : products.value.filter(p => p.preferred_type === modalType.value)
})

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/v1/products/products/')
  productsRaw.value = res.data
  products.value = buildFullProducts(res.data)
})
</script>

<style scoped>
.main-title {
  font-size: 2.3rem;
  font-family: 'Pretendard', sans-serif;
  font-weight: 800;
  border-bottom: 3px solid #e0e0e0;
  padding-bottom: 0.5rem;
  margin-bottom: 2rem;
}

.product-wrapper {
  font-family: 'Pretendard', sans-serif;
}
.top-form {
  background-color: #fafafa;
  border: 1.5px solid #cccccc;
  border-radius: 12px;
}

.recommend-btn {
  background-color: #f37075; /* 예: 주황색 */
  color: white;
  font-weight: bold;
  border: none;
  padding: 0.75rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.carousel-control-prev,
.carousel-control-next {
  width: 4rem;
  top: 35%;
  transform: translateY(-50%);
  z-index: 10;
}

/* 배경색/모양 유지 */
.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: rgba(100, 100, 100, 0.6);
  border-radius: 50%;
  background-size: 60% 60%;
  background-repeat: no-repeat;
  background-position: center;
  width: 2.5rem;
  height: 2.5rem;
}

.carousel-control-prev {
  left: -2.5rem;
}
.carousel-control-next {
  right: -2.5rem;
}

.divider {
  border: none;
  height: 2px;
  background-color: #e0e0e0;
  margin-top: 4rem;  /* 위쪽 간격 */
  margin-bottom: 4rem; /* 아래쪽 간격 */
}

#bankCarousel {
  margin-bottom: 3rem; /* ✅ 은행 카드와 테이블 사이 간격 추가 */
}

.tabs button {
  padding: 0.5rem 1.2rem;
  border: 2px solid #2F9E44;
  border-radius: 8px;
  background-color: white;
  color: #2F9E44;
  cursor: pointer;
  font-weight: bold;
  margin-right: 1rem; /* ✅ 버튼 간 간격 추가 */

}
.tabs .active {
  background-color: #2F9E44;
  color: white;
}
.product-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}
.product-table th,
.product-table td {
  border: 1px solid #ccc;
  padding: 0.6rem;
  text-align: center;
}
.product-table th {
  background-color: #e9fbe9;
  color: black;
}

.product-table tbody tr:hover td:first-child {
  background-color: #f9f9f9; /* 은은한 회색 */
  cursor: pointer;
}

.product-table tbody tr:hover td:first-child .link {
  color: #1b5e20; /* 짙은 초록 */
  text-decoration: underline;
}

.recommend-text {
  color: #276f3d;
  font-weight: 500;
}
.link {
  color: black;
  font-weight: solid;
  text-decoration: none;
}

.custom-modal-btn {
  background-color: #2F9E44;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.2s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.custom-modal-btn:hover {
  background-color: #276f3d;
  transform: translateY(-2px);
}

</style>