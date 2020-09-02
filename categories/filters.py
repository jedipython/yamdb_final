from django_filters import rest_framework as filters
from .models import Title


class TitlesFilter(filters.FilterSet):
    category = filters.CharFilter('category__slug')
    genre = filters.CharFilter('genre__slug')
    name = filters.CharFilter('name', lookup_expr='contains')

    class Meta:
        fields = ['name', 'category', 'genre', 'year', ]
        model = Title
