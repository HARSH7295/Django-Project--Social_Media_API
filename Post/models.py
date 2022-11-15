from django.db import models
from User.models import CustomUser
import uuid
# Create your models here.
class Post(models.Model):
    postId = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    postedBy = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    img = models.ImageField()
    likedBy = models.ManyToManyField(CustomUser,related_name='likedBy')
