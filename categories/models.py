from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=400, blank=True)
    year = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    genre = models.ManyToManyField(Genre)
