from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Review
from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug
        }


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug
        }


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = GenreField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)
    rating = serializers.SerializerMethodField(method_name='calculate_rating')

    def calculate_rating(self, title):
        title_reviews = Review.objects.filter(review_object=title)
        if title_reviews.count() > 0:
            return title_reviews.aggregate(Avg('score'))['score__avg']
        return None

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title
