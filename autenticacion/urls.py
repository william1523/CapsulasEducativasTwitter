from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import InicioSesionView,finalizarSesion

app_name = 'autentication'
urlpatterns = [
    path('accounts/login/',InicioSesionView, name="login"),
    path('logout/',login_required( finalizarSesion ), name="logout")
]
