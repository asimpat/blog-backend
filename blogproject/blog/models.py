from django.db import models
from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    owner = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="posts", default="user"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="user")
    phone = models.TextField(blank=True, null=False)
    country = models.TextField(blank=True, null=False)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
