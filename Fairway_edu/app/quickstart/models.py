from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.conf import settings

class Consultant(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    consultant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    

class Folder(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    consultant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Changed related_name to avoid clash with Picture's reverse relationship
    pictures = models.ManyToManyField('Picture', related_name='folders', blank=True)

    def __str__(self):
        return self.name

class Picture(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='picture_set')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pictures/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Services(models.Model):
    title=models.CharField(max_length=100,null=False)
    description=models.TextField(blank=True, null=False)
    consultant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Services')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    