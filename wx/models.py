from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64)
    wx_id = models.CharField(max_length=64,default='none')
    phone = models.CharField(max_length=64)
    refresh_token = models.CharField(max_length=64,default='none')
    password = models.CharField(max_length=200)
    openid = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    headimgurl = models.CharField(max_length=200)
    privilege = models.CharField(max_length=200)
    unionid = models.CharField(max_length=200)

    def __str__(self):
        return self.username