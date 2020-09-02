from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from categories.models import Title


class Review(models.Model):
    review_object = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'author',
                    'review_object',
                ),
                name='unique_review'
            ),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
