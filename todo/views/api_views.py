from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..models import Todo
from ..serializers import TodoSerializer
from interaction.models import TodoLike, TodoBookmark, TodoComment
from django.db.models import Q


# ---------------------------------------------------------
# 페이지네이션 설정
# ---------------------------------------------------------
class TodoListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 50


# ---------------------------------------------------------
# 핵심 ViewSet
# ---------------------------------------------------------
class TodoViewSet(viewsets.ModelViewSet):

    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TodoListPagination

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(Q(is_public=True) | Q(user=user)).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # -----------------------------------------------------
    # list API 커스터마이징
    # -----------------------------------------------------
    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={"request": request},
            )
            return Response(
                {
                    "data": serializer.data,
                    "current_page": int(request.query_params.get("page", 1)),
                    "page_count": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link() is not None,
                    "previous": self.paginator.get_previous_link() is not None,
                }
            )

        serializer = self.get_serializer(
            qs,
            many=True,
            context={"request": request},
        )
        return Response(
            {
                "data": serializer.data,
                "current_page": 1,
                "page_count": 1,
                "next": False,
                "previous": False,
            }
        )

    # -----------------------------------------------------
    # 좋아요 토글 API
    # POST /todo/viewsets/view/<id>/like/
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        todo = self.get_object()
        user = request.user

        obj, created = TodoLike.objects.get_or_create(todo=todo, user=user)

        if created:
            liked = True
        else:
            obj.delete()
            liked = False

        like_count = TodoLike.objects.filter(todo=todo).count()

        return Response({"liked": liked, "like_count": like_count})

    # -----------------------------------------------------
    # 북마크 토글 API
    # POST /todo/viewsets/view/<id>/bookmark/
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        todo = self.get_object()
        user = request.user

        obj, created = TodoBookmark.objects.get_or_create(todo=todo, user=user)

        if created:
            bookmarked = True
        else:
            obj.delete()
            bookmarked = False

        bookmark_count = TodoBookmark.objects.filter(todo=todo).count()

        return Response({"bookmarked": bookmarked, "bookmark_count": bookmark_count})

    # -----------------------------------------------------
    # 댓글 등록 API
    # POST /todo/viewsets/view/<id>/comments/
    # -----------------------------------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        todo = self.get_object()
        user = request.user

        content = (request.data.get("content") or "").strip()

        if not content:
            return Response({"detail": "content is required"}, status=400)

        TodoComment.objects.create(todo=todo, user=user, content=content)

        comment_count = TodoComment.objects.filter(todo=todo).count()

        return Response({"comment_count": comment_count})
