from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import uuid


# Create your models here.

# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.username
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user
    
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.user
    
class Like(models.Model):
    postId = models.CharField(max_length=500)
    liker = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    
    
    def __str__(self):
        return self.owner