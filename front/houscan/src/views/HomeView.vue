<template>
  <div>
    <!-- 🔹 상단 메인 배너 -->
    <div class="home-wrapper">
      <div class="content-box">
        <h1 class="slogan">
          청약의 시작과 끝, <br />
          <span class="highlight">HOUSCAN</span>이 함께합니다.
        </h1>
        <p class="sub-slogan">
          <br>
          맞춤형 예·적금 추천부터 청약 일정 관리까지 도와주는
          <strong>올인원 주택 청약 지원 플랫폼</strong>입니다. <br>

          처음 청약을 준비하는 분들도,
          지금 바로 HOUSCAN과 함께 시작해요 ! </p>
      </div>
    </div>

    <!-- 🔸 서비스 소개 영역 -->
    <section class="services-section">
      <div class="section-title">HOUSCAN이 제공하는 서비스</div>

      <div class="service-line" v-for="(service, index) in services" :key="index">
        <div class="service-block" :class="{ 'reverse': index % 2 === 1 }" @click="goTo(service.path)">
          <img :src="service.image" class="service-image" alt="서비스 이미지" />
          <div class="service-content" v-scroll-fade>
            <h3>{{ service.title }}</h3>
            <p>
              {{ service.description }}
            </p>
          </div>
        </div>
        <hr class="divider" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
const router = useRouter()

const goTo = (path) => {
  router.push(path)
}

const services = [
  {
    title: 'AI 기반 청약 가점 분석',
    description: 'AI 알고리즘을 활용해 청약 가점을 분석하고, 지역·유형별 경쟁률 데이터를 기반으로 당첨 가능성을 예측해드립니다.',
    image: new URL('@/assets/section1.jpg', import.meta.url).href,
    path: '/calculate',
  },
  {
    title: '맞춤형 예·적금 상품 추천',
    description: '목표 자산과 투자 기간을 입력하면, 수익률·안정성을 고려한 최적의 예·적금 상품을 자동 추천해드립니다.',
    image: new URL('@/assets/section2.jpg', import.meta.url).href,
    path: '/product',
  },
  {
    title: '실시간 청약 공고 확인',
    description: '현재 진행 중인 청약 공고를 한눈에 파악하고, 관심 있는 공고를 저장하여 빠르게 접근할 수 있습니다.',
    image: new URL('@/assets/section3.jpg', import.meta.url).href,
    path: '/houselist',
  },
  {
    title: '청약 경쟁률 데이터 시각화',
    description: '지역별·기간별 청약 경쟁률 데이터를 시각화하여, 주요 트렌드와 통계 흐름을 직관적으로 제공합니다.',
    image: new URL('@/assets/section4.jpg', import.meta.url).href,
    path: '/competition',
  },
]


// ✅ Scroll Trigger Directive
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('show')
      }
    })
  }, { threshold: 0.1 })

  document.querySelectorAll('[v-scroll-fade], .service-content').forEach(el => {
    el.classList.add('before-fade')
    observer.observe(el)
  })
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

.home-wrapper {
  position: relative;
  height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  padding-left: 5vw;
  overflow: hidden;
}

.home-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/main-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: grayscale(20%) brightness(0.6) saturate(110%);
  z-index: 0;
}

.content-box {
  position: relative;
  z-index: 1;
  text-align: left;
}

.slogan {
  font-size: 4.2rem;
  line-height: 1.4;
  color: white;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
}

.sub-slogan{
  font-size : 1.3rem;
  color:white;
  font-family: 'Inter'
}

.highlight {
  color: #a1f0a1;
  font-weight: 800;
}

.services-section {
  padding: 12rem 8vw;
  z-index: 1;
  max-width: 1400px;
  margin: -4rem auto 0;
}

.section-title {
  font-size: 2.8rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 8rem;
  color: #1b5550;
  font-family: 'Inter', sans-serif;
}

.service-line {
  margin-bottom: 10rem;
  background-color: #fafafa;

}

.service-block {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 6rem;
  transition: transform 0.3s ease, background-color 0.3s ease;
  border-radius: 1rem;
}

.service-block.reverse {
  flex-direction: row-reverse;
}

.service-block:hover {
  transform: translateY(-4px);
  background-color: #f9f9fc;
}

.divider {
  border: none;
  height: 1px;
  background-color: #e3e6ea;
  margin-top: 3rem;
}

.service-image {
  width: 340px;
  height: 340px;
  object-fit: cover;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.service-content h3 {
  font-size: 2.6rem;
  color: #212529;
  margin-bottom: 1.8rem;
  font-weight: 700;
  font-family: 'Inter', sans-serif;
}

.service-content p {
  font-size: 1.4rem;
  color: #495057;
  line-height: 2;
  max-width: 640px;
  font-weight: 400;
  font-family: 'Inter', sans-serif;
}

/* ✅ Scroll Fade Effect */
.before-fade {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.6s ease-out;
}

.show {
  opacity: 1;
  transform: translateY(0);
}

.service-content p {
  font-size: 1.25rem;
  color: #495057;
  line-height: 1.8;
  font-weight: 400;
  word-break: keep-all;       /* ✅ 단어 중간에서 끊기지 않게 */
  white-space: normal;        /* ✅ 자연스럽게 줄바꿈 */
  max-width: 640px;
}
</style>