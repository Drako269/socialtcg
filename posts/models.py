# posts/models.py
from django.db import models
from users.models import CustomUser

class Post(models.Model):
    # Tipos de publicación
    TYPE_CHOICES = [
        ('registered', 'Carta Registrada'),
        ('unregistered', 'Carta No Registrada'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # Para cartas registradas: vinculamos a una carta oficial
    # Usaremos un campo genérico para soportar ambos juegos
    game = models.CharField(
        max_length=20,
        choices=[('pokemon', 'Pokémon'), ('yugioh', 'Yu-Gi-Oh!')],
        blank=True,
        null=True
    )
    card_id = models.IntegerField(blank=True, null=True)  # ID en la base externa
    card_name = models.CharField(max_length=200, blank=True)  # Nombre oficial

    # Foto personal de la carta (obligatoria en ambos tipos)
    photo = models.ImageField(upload_to='post_photos/', blank=False)

    # Descripción (ej: "¡Mi Charizard de 1999!", "Carta que gané en el torneo")
    description = models.TextField(max_length=500, blank=True)

    # ¿Está a la venta?
    for_sale = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Publicación'
        verbose_name_plural = 'Publicaciones'

    def __str__(self):
        return f"{self.user.username}: {self.card_name or 'Carta no registrada'}"

    @property
    def is_registered(self):
        return self.type == 'registered'

    def get_card_object(self):
        """
        Devuelve el objeto de carta real desde la base externa.
        Útil para mostrar info oficial.
        """
        from cards.models import PokemonCard, YuGiOhCard

        if not self.is_registered:
            return None

        try:
            if self.game == 'pokemon':
                return PokemonCard.objects.using('pokemon_db').get(id=self.card_id)
            elif self.game == 'yugioh':
                return YuGiOhCard.objects.using('yugioh_db').get(id=self.card_id)
        except:
            return None
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Me gusta'),
        ('awesome', '¡Impresionante!'),
        ('rare', '¡Qué rara!'),
        ('want', 'La quiero'),
        ('fire', '🔥'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evita que un usuario reaccione varias veces al mismo post
        unique_together = ('user', 'post')
        verbose_name = 'Reacción'
        verbose_name_plural = 'Reacciones'

    def __str__(self):
        return f"{self.user.username} → {self.get_reaction_type_display()} en {self.post.card_name}"