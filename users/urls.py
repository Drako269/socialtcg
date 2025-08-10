# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

# Solo necesitas esta línea vacía por ahora si no tienes vistas
urlpatterns = [
    # Ejemplo futuro:
    # path('login/', auth_views.LoginView.as_view(), name='login'),
]