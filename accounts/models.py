from django.db import models
from django.contrib.auth.models import User


def user_avatar_path(instance, filename):
    return f'avatars/{instance.user.username}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default.jpg')
    bio = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username
