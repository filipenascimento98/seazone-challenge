from rest_framework import routers
from django.urls import path, include

from api.views.imovel import ImovelView


router = routers.DefaultRouter()
router.register(r'imovel', ImovelView, basename='imovel')

urlpatterns = router.urls