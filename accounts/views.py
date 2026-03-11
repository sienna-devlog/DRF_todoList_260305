from django.contrib.auth import logout

# DRF APIView 사용
from rest_framework.views import APIView

# API 응답 객체
from rest_framework.response import Response

# HTTP 상태 코드
from rest_framework import status

# 모든 사용자 접근 허용
from rest_framework.permissions import AllowAny, IsAuthenticated

# 회원가입 데이터 검증 Serializer
from .serializers import SignupSerializer


# -----------------------------
# 회원가입 API (JWT/세션과 무관하게 그대로 사용)
# -----------------------------
class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


# -----------------------------
#     ⚠️ 전환기 임시 로그아웃(세션 정리용)
#    - JWT 환경에서 '로그아웃'은 보통 프론트에서 토큰 삭제로 처리합니다.
#    - 그래도 혹시 남아있을 수 있는 세션을 logout(request)로 정리해줍니다.
# -----------------------------
class SessionLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃(세션 정리)"}, status=status.HTTP_200_OK)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        )
