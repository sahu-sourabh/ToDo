from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = CloudinaryField('profile_pic')
    
    def __str__(self):
        return f'{self.user.username} Profile'
