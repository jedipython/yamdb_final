from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api_yamdb.permissions import IsAuthorOrReadOnly, has_role
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from categories.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrReadOnly | has_role('Moderator'),
        IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            review_object=title
        )

    def get_queryset(self):
        return Review.objects.filter(review_object__pk=self.kwargs['title_id'])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly | has_role('Moderator'),
        IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        return Comment.objects.filter(
            review__review_object__pk=self.kwargs['title_id'],
            review__pk=self.kwargs['review_id']
        )
