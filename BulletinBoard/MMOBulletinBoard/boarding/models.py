from django.db import models
from django.contrib.auth.models import User

from boarding.resources import *


class Post(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=2,
                               choices=CATEGORY,
                               default=tanks)
    cre_dt = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=128)
    content = models.TextField()

    def __str__(self):
        return f'{self.header.title()}: {self.content}'


class Response(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    cre_dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    applied = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username.title()}: {self.text}'

    def apply(self):
        self.applied = True
        self.save()
