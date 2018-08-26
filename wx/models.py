from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64, default='none')
    phone = models.CharField(max_length=64, default='none')
    refresh_token = models.CharField(max_length=64, default='none')
    password = models.CharField(max_length=200, default='none')
    openid = models.CharField(max_length=200, default='none')
    nick = models.CharField(max_length=60, default=None)
    avatar = models.CharField(max_length=200)
    info = models.TextField(max_length=600, default=None)
    union_id = models.CharField(max_length=200 ,default='none')

    def __str__(self):
        return self.username
