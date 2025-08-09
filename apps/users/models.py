from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username