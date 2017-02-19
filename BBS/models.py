from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,AbstractUser
from django.contrib.auth.models import Permission
# Create your models here.

class BBS(models.Model):
    cate=models.ForeignKey('Category',default=7)
    title=models.CharField(max_length=64,)
    summary=models.CharField(max_length=256,blank=True,null=True)
    content=models.TextField()
    author = models.ForeignKey("BBS_user")
    view_count=models.IntegerField(blank=True,null=True)
    ranking=models.IntegerField(blank=True,null=True)
    create_at=models.DateTimeField(blank=True,null=True)
    update_at=models.DateTimeField(blank=True,null=True)
    def __unicode__(self):
        return self.title
    pass

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    administrator=models.ForeignKey('BBS_user')
    def __unicode__(self):
        return self.name
class BBS_user(models.Model):
    user=models.OneToOneField(User)
    signature=models.CharField(max_length=128,blank=True,null=True,default='this guy is to lazy to leave any thing here.')
    photo=models.ImageField(blank=True,null=True)
    photo=models.ImageField(upload_to='upload_imgs/',default='upload_imgs/user-1.jpg')
    def __unicode__(self):
        return self.user.username
    pass



















