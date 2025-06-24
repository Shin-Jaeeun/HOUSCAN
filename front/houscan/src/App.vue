<template>
  <div>
    <header :class="['navbar', { scrolled: isScrolled || isHovered }]">
      <RouterLink to="/">
        <img src="@/assets/logo.png" alt="logo" class="logo" />
      </RouterLink>

      <!-- 메뉴 -->
      <div class="menu-wrapper">
        <nav class="menu">
          <div class="menu-item" @click.stop="toggleMenu('자산 준비')">
            <span class="menu-label">자산 준비</span>
            <div class="custom-dropdown" v-if="activeMenu === '자산 준비'">
              <RouterLink to="/calculate">청약 가점 예측</RouterLink>
              <RouterLink to="/product">예적금 상품 추천</RouterLink>
            </div>
          </div>
          <div class="menu-item" @click.stop="toggleMenu('청약 공고')">
            <span class="menu-label">청약 공고</span>
            <div class="custom-dropdown" v-if="activeMenu === '청약 공고'">
              <RouterLink to="/houselist">진행 중인 청약</RouterLink>
              <RouterLink to="/competition">지난 경쟁률 확인</RouterLink>
            </div>
          </div>
          <div class="menu-item" @click.stop="toggleMenu('커뮤니티')">
            <span class="menu-label">커뮤니티</span>
            <div class="custom-dropdown" v-if="activeMenu === '커뮤니티'">
              <RouterLink to="/community">커뮤니티</RouterLink>
            </div>
          </div>
        </nav>
      </div>

      <!-- 로그인 / 프로필 -->
      <div class="login-btn">
        <RouterLink v-if="!authStore.isLogin" to="/login" class="login-link">로그인</RouterLink>
        <div v-else class="user-info-wrapper" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
        <div class="user-info">
          <span><strong>{{ authStore.username }}</strong> 님</span>
          <img src="@/assets/profile.png" class="avatar" />

          <div class="alarm-wrapper" @click.stop="toggleAlarm">
            <img src="@/assets/alram.png" alt="알림" class="alarm-icon" />
            <span class="alarm-badge" v-if="visibleNotices.length > 0">{{ visibleNotices.length }}</span>
          </div>
        </div>

          <div class="alarm-dropdown" v-if="showAlarm">
            <h4>📢 마감 임박 공고</h4>
            <ul>
              <template v-if="visibleNotices.length > 0">
                <li v-for="notice in visibleNotices" :key="notice.id">
                  <div class="notice-title">{{ notice.title }}</div>
                  <div class="notice-dday">{{ calcDday(notice.deadline) }}</div>
                </li>
              </template>
              <template v-else>
                <li><em style="color: gray;">임박한 공고가 없습니다.</em></li>
              </template>
            </ul>
          </div>

          <div class="dropdown-menu" v-if="showDropdown">
            <RouterLink to="/mypage/update">회원정보 수정</RouterLink>
            <RouterLink to="/mypage/favorite">찜한 목록</RouterLink>
            <button @click="logout">로그아웃</button>
          </div>
        </div>
      </div>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

const showDropdown = ref(false)
const showAlarm = ref(false)
const favoriteNotices = ref([])
const isScrolled = ref(false)
const isHovered = ref(false)
const activeMenu = ref(null)

const toggleMenu = (menuName) => {
  activeMenu.value = activeMenu.value === menuName ? null : menuName
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10
}

onMounted(() => {
  authStore.initializeAuth()
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('click', () => (activeMenu.value = null))
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

const logout = () => {
  authStore.logout()
  axios.defaults.headers.common.Authorization = ''
  router.push('/login')
}

const toggleAlarm = async () => {
  showAlarm.value = !showAlarm.value
  if (showAlarm.value) {
    try {
      const res = await axios.get('/api/v1/houses/favorites/?flat=true', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      })
      favoriteNotices.value = res.data
    } catch (err) {
      console.error('📛 찜한 공고 불러오기 실패:', err)
    }
  }
}

const calcDday = (deadline) => {
  const today = new Date()
  const end = new Date(deadline)
  const diffTime = end - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 ? `D-${diffDays}` : '마감'
}

const visibleNotices = computed(() =>
  favoriteNotices.value.filter(
    (n) => n && n.deadline && calcDday(n.deadline) !== '마감'
  )
)
</script>

<style scoped>
.logo {
  height: 80px;
  max-height: 100%;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  background-color: white;
  min-height: 80px;
  border-bottom: 1px solid #e0e0e0;
}

.menu-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
}

.menu {
  display: flex;
  gap: 4rem;
  font-size: 1rem;
}

.menu-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu-label {
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
  font-size: 1.1rem;
  cursor: pointer;
}

.custom-dropdown {
  position: absolute;
  top: 3.2rem;
  background-color: #2f9e44;
  border-radius: 6px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  padding: 1.2rem 1.6rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  z-index: 100;
  min-width: 220px;
}

.custom-dropdown a,
.dropdown-menu a,
.dropdown-menu button {
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  text-decoration: none;
  text-align: center;
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Pretendard', sans-serif;
}

.custom-dropdown a:hover,
.dropdown-menu a:hover,
.dropdown-menu button:hover {
  text-decoration: underline;
}

.login-btn {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
}

.login-link {
  background-color: white;
  border: 2px solid #005600;
  color: #005600;
  padding: 0.6rem 1.6rem;
  border-radius: 3rem;
  font-weight: bold;
  text-decoration: none;
  font-size: 1.3rem;
  transition: background-color 0.3s;
}

.login-link:hover {
  background-color: #e6ffe6;
}

.alarm-dropdown {
  position: absolute;
  top: 100px;
  right: 60px;
  background: #ffffff;
  border: 2px solid #f37075;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  padding: 1.5rem 1.8rem;
  min-width: 300px;
  z-index: 1000;
  font-size: 1.1rem;
  word-break: break-word;
}

.alarm-dropdown h4 {
  margin-bottom: 1rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #f37075;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alarm-dropdown ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alarm-dropdown li {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.alarm-dropdown li:last-child {
  border-bottom: none;
}


.user-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: relative;
}

.user-info span {
  font-size: 1.1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-weight: bold;
  color: black;
}

.user-info span strong {
  font-size: 1.5rem;
  font-family: 'Arial Black', Gadget, sans-serif;
  color: #2f9e44;
}

.user-info img {
  width: 40px;
  height: 40px;
  object-fit: cover;
  /* filter: drop-shadow(0 0 1px #2f9e44); */
}


.avatar {
  /* border-radius: 50%;
  border: 2px solid #2f9e44;
  background-color: white; */
  cursor: pointer;
}


.alarm-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  margin-right: 4px;
  cursor: pointer;
}

.alarm-wrapper {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.alarm-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background-color: #20c997; /* ✅ 청록 계열 */
  color: white;
  font-size: 0.7rem;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 50%;
  z-index: 10;
  line-height: 1;
}



.user-info-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  z-index: 999;
}

.dropdown-menu {
  position: absolute;
  top: 3.2rem;
  right: 0;
  background-color: #2f9e44;
  border-radius: 6px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  padding: 1.2rem 1.6rem;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  min-width: 220px;
  z-index: 999;
}

.notice-title {
  font-weight: 500;
  margin-bottom: 0.2rem;
  line-height: 1.4;
  color: #222;
  white-space: normal;
  word-break: break-word;
}

.notice-dday {
  align-self: flex-end;
  color: red;
  font-weight: bold;
  font-size: 1.1rem;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
}
</style>

