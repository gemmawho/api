from django.db import models

from users.models import User
from .validators import validate_year, validate_score


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ('name',)


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(validators=[validate_year], db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True)
    description = models.TextField(blank=True)


class Review(models.Model):
    title = models.ForeignKey(Title, related_name='title_reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user_reviews', on_delete=models.CASCADE)
    text = models.TextField()
    score = models.IntegerField(validators=[validate_score])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ('title', 'author')


class Comment(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, related_name='review_comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    author = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
