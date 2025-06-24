<template>
  <div class="bg-light py-5 mt-5 pt-5">
    <!-- 📊 제목 -->
    <h2 class="main-title text-center">청약 경쟁률 시각화</h2>

    <!-- 🔍 선택 필터 영역 -->
    <div class="container">
      <form class="row gy-3 gx-4 align-items-end filter-form">
        <div class="col-md-4 form-group">
          <label for="regionSelect" class="form-label fs-5">지역</label>
          <select id="regionSelect" class="form-select form-select-sm fs-6" v-model="selectedRegion">
            <option disabled value="">-- 선택 --</option>
            <option v-for="r in regionOptions" :key="r">{{ r }}</option>
          </select>
        </div>
        <div class="col-md-3 form-group">
          <label for="startDate" class="form-label fs-5">시작 연도/월</label>
          <input id="startDate" type="month" class="form-control form-control-sm fs-6" v-model="startMonth" />
        </div>
        <div class="col-md-3 form-group">
          <label for="endDate" class="form-label fs-5">종료 연도/월</label>
          <input id="endDate" type="month" class="form-control form-control-sm fs-6" v-model="endMonth" />
        </div>
        <div class="col-md-2 d-grid">
          <button class="btn btn-primary btn-sm fw-semibold fs-6" type="button" @click="fetchData">불러오기</button>
        </div>
      </form>
    </div>

    <!-- 📊 그래프 카드 -->
    <div class="container mb-5">
      <div class="card shadow-sm p-4">
        <div class="chart-wrapper">
          <canvas id="competitionChart"></canvas>
        </div>
        <p v-if="chartData.length === 0" class="text-muted text-center mt-4 fst-italic">
          조건을 선택하고 데이터를 불러오세요.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const selectedRegion = ref('')
const startMonth = ref('2020-01')
const endMonth = ref('2023-12')
const chartData = ref([])
const chartInstance = ref(null)

const regionOptions = [
  '서울', '부산', '대구', '인천', '광주',
  '대전', '울산', '세종', '경기', '강원',
  '충북', '충남', '전북', '전남', '경북',
  '경남', '제주'
]

const fetchData = async () => {
  if (!selectedRegion.value || !startMonth.value || !endMonth.value) return
  try {
    const url = `http://localhost:8000/api/v1/houses/competition/filter/?region=${selectedRegion.value}&start=${startMonth.value}&end=${endMonth.value}`
    const res = await axios.get(url)
    chartData.value = res.data.filter(item => item.special_competition_rate >= 0 && item.general_competition_rate >= 0)

    await nextTick()
    drawChart(chartData.value)
  } catch (err) {
    console.error('❌ 경쟁률 데이터 로드 실패:', err)
    alert("데이터를 불러오는 중 오류가 발생했습니다.")
  }
}

const drawChart = (data) => {
  const ctx = document.getElementById('competitionChart')?.getContext('2d')
  if (!ctx) return

  const labels = data.map(item => {
    const [year, month] = item.year_month.split('-')
    return `${year}.${month}`
  })

  const specialRates = data.map(item => item.special_competition_rate)
  const generalRates = data.map(item => item.general_competition_rate)

  if (chartInstance.value) chartInstance.value.destroy()

  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: '특별공급 경쟁률',
          data: specialRates,
          borderColor: '#ff787b',
          backgroundColor: '#ff787b',
          fill: false,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 3
        },
        {
          label: '일반공급 경쟁률',
          data: generalRates,
          borderColor: '#6995eb',
          backgroundColor: '#6995eb',
          fill: false,
          tension: 0.4,
          pointRadius: 0,
          borderWidth: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: {
              size: 16,
              weight: '600'
            },
            color: '#333'
          }
        },
        title: {
          display: true,
          text: `${selectedRegion.value} 경쟁률 추이`,
          font: {
            size: 22,
            weight: 'bold'
          },
          color: '#222'
        },
        tooltip: {
          callbacks: {
            label: (context) => ` ${context.dataset.label}: ${context.parsed.y}배`
          }
        }
      },
      onClick: (e, elements) => {
        if (elements.length > 0) {
          const chart = chartInstance.value
          const idx = elements[0].index
          const datasetIdx = elements[0].datasetIndex
          const label = chart.data.labels[idx]
          const value = chart.data.datasets[datasetIdx].data[idx]
          const datasetLabel = chart.data.datasets[datasetIdx].label
          alert(`${label} (${datasetLabel}): ${value}배`)
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: '경쟁률 (배)',
            font: {
              size: 16,
              weight: 'bold'
            }
          },
          grid: {
            display: false
          }
        },
        x: {
          ticks: {
            font: {
              size: 10
            },
            maxRotation: 60,
            autoSkip: true,
            maxTicksLimit: 20
          },
          grid: {
            display: false
          }
        }
      }
    }
  })
}

onMounted(() => {
  selectedRegion.value = '서울'
  fetchData()
})
</script>

<style scoped>

.main-title {
  font-size: 2rem;
  font-family: 'Pretendard', sans-serif;
  font-weight: 800;
  padding-bottom: 0.5rem;
  margin-bottom: 2rem;
}

.chart-wrapper {
  position: relative;
  height: 600px;
  background-color: #ffffff;
  border-radius: 0.5rem;
  padding: 2rem;
  box-shadow: 0 0 0 transparent;
  z-index: 1;
  margin-top: 1rem;
}

.filter-form {
  background-color: #ffffff;
  padding: 2.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.filter-form .form-group {
  flex: 1 1 220px;
  min-width: 200px;
}

.filter-form button,
.container .btn.btn-primary {
  background-color: #f37075 !important;
  border-color: #f37075 !important;
  color: white;
}
</style>