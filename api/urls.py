from rest_framework import routers
from django.urls import path, include

from api.views.imovel import ImovelView
from api.views.anuncio import AnuncioView
from api.views.reserva import ReservaView


router = routers.DefaultRouter()
router.register(r'imovel', ImovelView, basename='imovel')
router.register(r'anuncio', AnuncioView, basename='anuncio')
router.register(r'reserva', ReservaView, basename='reserva')

urlpatterns = router.urls