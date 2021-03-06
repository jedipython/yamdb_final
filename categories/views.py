from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from api_yamdb.permissions import has_role

from .filters import TitlesFilter
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (has_role('Administrator', read_only=True),)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = "slug"


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (has_role('Administrator', read_only=True),)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (has_role('Administrator', read_only=True),)
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitlesFilter
