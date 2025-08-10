# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Campos adicionales para completar el perfil
    first_name = models.CharField(max_length=30, blank=False)  # obligatorio
    last_name = models.CharField(max_length=30, blank=False)   # obligatorio
    country = models.CharField(max_length=50, blank=False)
    ROLE_CHOICES = [
        ('collector', 'Coleccionista'),
        ('player', 'Jugador'),
        ('seller', 'Vendedor'),
        ('both', 'Coleccionista y Vendedor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)

    # Para saber si el usuario puede publicar
    is_complete = models.BooleanField(default=False, help_text="Indica si el usuario completó los datos para publicar.")

    # Relación de seguidores (self-referential)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Marcar como completo si tiene los campos necesarios
        if self.first_name and self.last_name and self.country and self.role:
            self.is_complete = True
        else:
            self.is_complete = False
        super().save(*args, **kwargs)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()