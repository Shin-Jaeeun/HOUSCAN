import { createRouter, createWebHistory } from 'vue-router'

// 메인페이지
import HomeView from '@/views/HomeView.vue'

// 계정 관련
import LoginView from '@/views/LoginView.vue'
import FindPasswordView from '@/views/FindPasswordView.vue'
import SignupView from '@/views/SignupView.vue'
import MyPageUpdateView from '@/views/MyPageUpdateView.vue'
import MyPageFavoriteView from '@/views/MyPageFavoriteView.vue'

// 가점계산기
import CalculateView from '@/views/CalculateView.vue'

// 예적금리스트
import ProductView from '@/views/ProductView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'

// 청약 공고
import HouseListView from '@/views/HouseListView.vue'
import HouseDetailView from '@/views/HouseDetailView.vue'

// 경쟁률
import CompetitionView from '@/views/CompetitionView.vue'

// 커뮤니티
import CommunityView from '@/views/CommunityView.vue'
import CommunityCreateView from '@/views/CommunityCreateView.vue'
import CommunityDetailView from '@/views/CommunityDetailView.vue'
import CommunityEditView from '@/views/CommunityEditView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/login/find', name: 'FindPassword', component: FindPasswordView },
  { path: '/signup', name: 'Signup', component: SignupView },
  { path: '/mypage/update', name: 'MyPageUpdate', component: MyPageUpdateView },
  { path: '/mypage/favorite', name: 'MyPageFavorite', component: MyPageFavoriteView },
  { path: '/calculate', name: 'Calculate', component: CalculateView },
  { path: '/product', name: 'ProductList', component: ProductView },
  { path: '/product/:id', name: 'ProductDetail', component: ProductDetailView, props: true },
  { path: '/houselist', name: 'HouseList', component: HouseListView },
  { path: '/houselist/:id', name: 'HouseDetail', component: HouseDetailView, props: true },
  { path: '/competition', name: 'Competition', component: CompetitionView },
  { path: '/community', name: 'Community', component: CommunityView },
  { path: '/community/create', name: 'CommunityCreate', component: CommunityCreateView },
  { path: '/community/:postId', name: 'CommunityDetail', component: CommunityDetailView, props: true },
  { path: '/community/:postId/edit', name: 'CommunityEdit', component: CommunityEditView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
