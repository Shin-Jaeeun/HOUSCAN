<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-box">
      <h3>전체 {{ type }} 상품 리스트</h3>
      <table class="product-table">
        <thead>
          <tr>
            <th>금융사</th>
            <th>상품명</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>24개월</th>
            <th>36개월</th>
            <th v-if="showRecommend">추천 설명</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.name + product.institution">
            <td>{{ product.institution }}</td>
            <td>
              <RouterLink :to="`/product/${product.id}`" class="link">
                {{ product.name }}
              </RouterLink>
            </td>
            <td>{{ product.rates?.[6] ?? '-' }}%</td>
            <td>{{ product.rates?.[12] ?? '-' }}%</td>
            <td>{{ product.rates?.[24] ?? '-' }}%</td>
            <td>{{ product.rates?.[36] ?? '-' }}%</td>
            <td v-if="showRecommend" class="recommend-text">{{ product.recommended_message }}</td>
          </tr>
        </tbody>
      </table>
      <button class="close-btn" @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: String,
  products: Array,
  showRecommend: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])
</script>
<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-box {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  max-height: 80vh;
  overflow-y: auto;
  width: 90%;
  max-width: 1000px;
  font-family: 'Pretendard', sans-serif;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
  margin-top: 1rem;
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

/* 상품명 셀 hover 시 회색 배경 */
.product-table tbody tr:hover td:nth-child(2) {
  background-color: #f9f9f9;
  cursor: pointer;
}

/* 링크 강조 */
.product-table tbody tr:hover td:nth-child(2) .link {
  color: #1b5e20;
  text-decoration: underline;
}

.recommend-text {
  color: #1b5e20;
  font-weight: 500;
}

.link {
  color: black;
  font-weight: solid;
  text-decoration: none;
}

.close-btn {
  margin-top: 1rem;
  background: #2F9E44;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>