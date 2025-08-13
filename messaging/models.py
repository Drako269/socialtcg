from django.db import models
from users.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"De {self.sender} a {self.recipient}"