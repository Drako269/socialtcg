# cards/urls.py
from django.urls import path
from . import views

app_name = 'cards'

urlpatterns = [
    path('test/', views.test_db_connection, name='test_db'),
    path('image/<str:game>/<int:card_id>/', views.card_image, name='card_image'),
]