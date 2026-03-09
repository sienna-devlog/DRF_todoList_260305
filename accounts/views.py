# Django 인증 관련 함수
# authenticate → 사용자 인증
# login → 세션 로그인 처리
# logout → 세션 로그아웃 처리
from django.contrib.auth import authenticate, login, logout

# DRF APIView 사용
from rest_framework.views import APIView

# API 응답 객체
from rest_framework.response import Response

# HTTP 상태 코드
from rest_framework import status

# 모든 사용자 접근 허용
from rest_framework.permissions import AllowAny

# 회원가입 데이터 검증 Serializer
from .serializers import SignupSerializer


# -----------------------------
# 회원가입 API
# -----------------------------
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


# -----------------------------
# 세션 로그인 API
# -----------------------------
class SessionLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response(
                {"detail": "아이디/비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)

        return Response({"detail": "로그인 성공"}, status=status.HTTP_200_OK)


# -----------------------------
# 세션 로그아웃 API
# -----------------------------
class SessionLogoutAPIView(APIView):

    def post(self, request):

        logout(request)

        return Response({"detail": "로그아웃"}, status=status.HTTP_200_OK)
