from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterAPIView, LoginAPIView, SendVerificationCodeAPIView, VerifyCodeAPIView, EmailCheckAPIView, ResetPasswordAPIView, UpdateNicknameAPIView,UpdatePasswordAPIView, CustomTokenRefreshView, DeleteAccountView,UserMeAPIView
router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email-check/', EmailCheckAPIView.as_view()),
    path('send-code/', SendVerificationCodeAPIView.as_view()),
    path('verify-code/', VerifyCodeAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('update-nickname/', UpdateNicknameAPIView.as_view()),
    path('update-password/', UpdatePasswordAPIView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('delete/', DeleteAccountView.as_view()),
    path('me/', UserMeAPIView.as_view(), name='user-me'),
]
