<template>
  <div class="container py-5 mt-5 pt-5">
    <h2 class="main-title text-center">청약 가점 계산기</h2>

    <!-- 가점 입력 폼 -->
    <div class="bg-light p-4 rounded shadow-sm mb-4">
      <div class="row g-3">
        <div class="col-md-4">
          <label for="homelessYears" class="form-label fw-semibold">무주택 기간</label>
          <select class="form-select" v-model="homelessYears" id="homelessYears">
            <option v-for="year in 16" :key="'homeless-' + year" :value="year - 1">{{ year - 1 }}년</option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="dependents" class="form-label fw-semibold">부양가족 수</label>
          <select class="form-select" v-model="dependents" id="dependents">
            <option v-for="count in 6" :key="'dependent-' + count" :value="count">{{ count }}명</option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="subscriptionYears" class="form-label fw-semibold">청약통장 가입기간</label>
          <select class="form-select" v-model="subscriptionYears" id="subscriptionYears">
            <option v-for="year in 18" :key="'subscription-' + year" :value="year - 1">{{ year - 1 }}년</option>
          </select>
        </div>
      </div>

      <div class="d-flex justify-content-center mt-4">
        <button class="btn fw-semibold btn-outline-dark px-4 py-2 rounded" @click="calculateScore">
          가점 계산하기
        </button>
      </div>

      <div class="bg-light rounded p-4 my-4 text-center shadow fade-in">
        <h4 class="fw-semibold mb-3 text-secondary">🎯 나의 청약 가점</h4>
        <p class="fs-3 fw-bold text-dark">
          총 가점은
          <span class="display-5 fw-bold" style="margin: 0 1rem; color: #2f9e44;">
            {{ score }}점
          </span>
          입니다
        </p>
      </div>
    </div>

    <!-- AI 분석 카드 -->
    <div class="card bg-white shadow-sm p-4">
      <h3 class="mb-3 fw-bold">📊 청약 경쟁률 분석</h3>
      <button class="btn fw-semibold text-white"
        style="background-color: #f37075; padding: 0.6rem 1.2rem; border: none; border-radius: 6px; font-size: 1rem;"
        @click="fetchAIAnalysis" :disabled="loading">
        분석받기
      </button>

      <template v-if="aiSections.analysis">
        <div class="ai-result-wrapper">
          <h4 class="fw-bold">AI 분석 결과</h4>

          <div class="ai-section">
            <div class="ai-number">1. 💡 청약 가점 분석</div>
            <div class="ai-text" v-html="formatBlock(aiSections.analysis)"></div>
          </div>

          <div class="ai-section">
            <div class="ai-number">2. 🏠 찜한 공고 분석 및 추천</div>
            <div class="ai-text" v-html="formatBlock(aiSections.recommendation)"></div>
          </div>

          <div class="ai-section">
            <div class="ai-number">3. 📌 전략 제안</div>
            <div class="ai-text" v-html="formatBlock(aiSections.strategy)"></div>
          </div>
        </div>
      </template>

    </div>

    <!-- 분석 중 모달 -->
    <div v-if="showLoadingModal" class="modal-overlay">
      <div class="modal-content modal-narrow">
        <img :src="loadingGif" alt="분석중" class="loading-gif" />
        <p class="modal-text">🏘️ HOUSCAN AI가 전략을 짜고 있습니다..</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import loadingGif from '@/assets/loading.gif'

const homelessYears = ref(0)
const dependents = ref(1)
const subscriptionYears = ref(0)
const score = ref(0)
const loading = ref(false)
const showLoadingModal = ref(false)

const aiSections = reactive({
  analysis: '',
  recommendation: '',
  strategy: ''
})

const calculateScore = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/v1/houses/score/', {
      homeless_years: homelessYears.value,
      num_dependents: dependents.value,
      subscription_years: subscriptionYears.value,
    })
    score.value = res.data.total_score
  } catch (err) {
    alert('가점 계산 실패')
    console.error(err)
  }
}

const formatBlock = (text) => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br/>')
}

const fetchAIAnalysis = async () => {
  try {
    showLoadingModal.value = true
    loading.value = true
    const token = localStorage.getItem('accessToken')
    const headers = { headers: { Authorization: `Bearer ${token}` } }

    const res = await axios.get('http://localhost:8000/api/v1/houses/favorites/', headers)
    const favorites = res.data.slice(0, 3)

    const aiRes = await axios.post('http://localhost:8000/api/v1/houses/ai/', {
      score: score.value,
      user_text: favorites.length > 0
        ? `[공고 목록]\n` + favorites.map(f => {
            const n = f.notice
            return `- ${n.title} | 지역: ${n.region} | 유형: ${n.category} | 마감일: ${n.apply_end}`
          }).join('\n')
        : "찜한 공고는 없습니다."
    }, headers)

    const result = aiRes.data.result
    const parts = result.split(/\n{2,}/g)
    aiSections.analysis = parts[0] || ''
    aiSections.recommendation = parts[1] || ''
    aiSections.strategy = parts.slice(2).join('\n\n') || ''
  } catch (err) {
    console.error('❌ AI 분석 실패', err)
    aiSections.analysis = 'AI 분석에 실패했습니다.'
  } finally {
    loading.value = false
    showLoadingModal.value = false
  }
}
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

.ai-result-wrapper {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid #dee2e6;
  margin-top: 2rem;
}

.ai-section {
  background: white;
  border: 1px solid #dee2e6;
  border-left: 4px solid #2f9e44;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.ai-number {
  font-weight: bold;
  color: #303030;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.ai-text {
  color: #333;
  font-size: 1rem;
  line-height: 1.7;
}

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

.modal-content {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  width: auto;
  min-width: 280px;
}

.modal-narrow {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.loading-gif {
  width: 180px;
  height: auto;
  margin-bottom: 1rem;
}

.modal-text {
  font-size: 1.1rem;
  color: #333;
  font-weight: 500;
}
</style>