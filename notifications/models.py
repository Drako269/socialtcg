from django.db import models
from users.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # quién hizo la acción
    verb = models.CharField(max_length=255)  # "te siguió", "comentó", "te dio like"
    
    # Para enlazar con cualquier modelo (Post, Comment, etc.)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target}"