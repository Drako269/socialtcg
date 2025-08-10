# cards/views.py
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.files.base import ContentFile
from .models import YuGiOhCard, PokemonCard

def test_db_connection(request):
    # Probar conexión con Yu-Gi-Oh! DB
    try:
        yugioh_cards = YuGiOhCard.objects.using('yugioh_db').all()[:5]  # 5 primeras cartas
    except Exception as e:
        yugioh_cards = []
        print("Error Yu-Gi-Oh! DB:", e)

    # Probar conexión con Pokémon DB
    try:
        pokemon_cards = PokemonCard.objects.using('pokemon_db').all()[:5]
    except Exception as e:
        pokemon_cards = []
        print("Error Pokémon DB:", e)

    return render(request, 'cards/test.html', {
        'yugioh_cards': yugioh_cards,
        'pokemon_cards': pokemon_cards
    })

def card_image(request, game, card_id):
    """
    Sirve la imagen BLOB de una carta de Yu-Gi-Oh! o Pokémon
    URL: /cards/image/pokemon/1/
         /cards/image/yugioh/50/
    """
    if game == 'pokemon':
        try:
            card = PokemonCard.objects.using('pokemon_db').get(id=card_id)
            image_data = card.image  # Esto es bytes
            content_type = 'image/png'  # Ajusta si hay JPEG
        except PokemonCard.DoesNotExist:
            raise Http404("Carta no encontrada")
    
    elif game == 'yugioh':
        try:
            card = YuGiOhCard.objects.using('yugioh_db').get(id=card_id)
            image_data = card.img_url  # bytes
            content_type = 'image/png'
        except YuGiOhCard.DoesNotExist:
            raise Http404("Carta no encontrada")
    
    else:
        raise Http404("Juego no válido")

    # Asegurarnos de que image_data sea bytes
    if isinstance(image_data, memoryview):
        image_data = image_data.tobytes()
    elif isinstance(image_data, str):
        # Si está como string, intentar convertir (poco común)
        try:
            image_data = image_data.encode('latin1')  # o 'utf-8'
        except:
            raise Http404("Datos de imagen inválidos")

    response = HttpResponse(content=image_data, content_type=content_type)
    return response