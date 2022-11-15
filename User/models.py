from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('Email Address'),unique=True,primary_key=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Profile(models.Model):
    profileId = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    about = models.CharField(max_length=200)
    profilePicture = models.ImageField()
    coverPicture = models.ImageField()
    followers = models.ManyToManyField(CustomUser,related_name='followers')
    followings = models.ManyToManyField(CustomUser,related_name='followings')