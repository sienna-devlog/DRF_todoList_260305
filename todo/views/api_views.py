from rest_framework import viewsets
from ..models import Todo
from ..serializers import TodoSerializer
from rest_framework.pagination import PageNumberPagination


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer


class TodoListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 50
