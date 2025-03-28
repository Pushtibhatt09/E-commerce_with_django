from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
