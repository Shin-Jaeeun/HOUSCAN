# accounts/views.py

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from .serializers import UserSerializer
from .serializers import CustomTokenObtainPairSerializer,CustomTokenRefreshSerializer
import random, string
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password,make_password
from .models import EmailVerification, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmailVerification 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class SendVerificationCodeAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': '이메일이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        code = str(random.randint(100000, 999999))  # 6자리로 변경
        print('📨 인증번호:', code)

        # DB 저장 (없으면 생성, 있으면 갱신)
        EmailVerification.objects.update_or_create(email=email, defaults={'code': code})

        try:
            # ✅ HTML 메일 본문 생성
            html_content = render_to_string('emails/verification_code.html', {'code': code})

            # ✅ 메일 객체 생성
            email_msg = EmailMultiAlternatives(
                subject='Houscan 가입 인증 코드입니다.',
                body='아래 인증번호를 가입 페이지에 입력해 주세요.',
                from_email='no-reply@houscan.com',  # 또는 settings.EMAIL_HOST_USER
                to=[email],
            )

            # ✅ HTML 본문 첨부
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

        except Exception as e:
            print('메일 전송 실패:', e)
            return Response({'error': '메일 전송 중 오류 발생'}, status=500)

        return Response({'message': '인증번호 발송 완료 ✅'})


class VerifyCodeAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            verify = EmailVerification.objects.get(email=email)
            if verify.code == code:
                return Response({'verified': True})
            else:
                return Response({'verified': False}, status=400)
        except EmailVerification.DoesNotExist:
            return Response({'verified': False}, status=400)

class EmailCheckAPIView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        exists = User.objects.filter(email=email).exists()
        return Response({'exists': exists})

class ResetPasswordAPIView(APIView):
    def put(self, request):
        email = request.data.get('email')
        new_password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            return Response({'message': '비밀번호 변경 완료'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': '존재하지 않는 이메일입니다'}, status=status.HTTP_404_NOT_FOUND)

# 닉네임 변경
class UpdateNicknameAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        password = request.data.get('password')
        new_username = request.data.get('username')

        if not check_password(password, user.password):
            return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.username = new_username
        user.save()
        return Response({'message': '닉네임이 변경되었습니다.'}, status=status.HTTP_200_OK)

# 비밀번호 변경
class UpdatePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not check_password(current_password, user.password):
            return Response({'error': '현재 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()
        return Response({'message': '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)
    

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        password = request.data.get('password')
        user = request.user

        if not check_password(password, user.password):
            return Response({'detail': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({'detail': '회원 탈퇴 완료'}, status=status.HTTP_204_NO_CONTENT)
    
    # views.py
class UserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

