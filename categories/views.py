from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Category, Genre, Title
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .filters import TitlesFilter
from api_yamdb.permissions import IsAuthorOrReadOnly, has_role
import django_filters


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
