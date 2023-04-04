from django.contrib import admin
from .models import  FollowersCount, Post, Like

# Register your models here.

# admin.site.register(Profile)
admin.site.register(FollowersCount)
admin.site.register(Post)
admin.site.register(Like)