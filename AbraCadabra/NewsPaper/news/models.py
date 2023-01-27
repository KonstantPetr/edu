from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from news.resources import *


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='authors')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_1 = Post.objects.filter(author=self.id).aggregate(Sum('rating'))['rating__sum']
        sum_2 = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        sum_3 = Comment.objects.filter(post__author=self.id).aggregate(Sum('rating'))['rating__sum']
        self.rating = sum_1 * 3 + sum_2 + sum_3
        self.save()

    def __str__(self):
        return self.user.username.title()


class Category(models.Model):

    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model, LikerMixIn):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    section = models.CharField(max_length=2,
                               choices=SECTION,
                               default=news)
    creation_dt = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:125] + '...'

    def __str__(self):
        return f'{self.header.title()}: {self.text[:50]}'


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model, LikerMixIn):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    creation_dt = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username.title()}: {self.text[:50]}'
