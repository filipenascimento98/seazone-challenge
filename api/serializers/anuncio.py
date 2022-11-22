from rest_framework import serializers
from api.models import Anuncio
from api.serializers.imovel import ImovelOutputSerializer

class AnuncioOutputSerializer(serializers.ModelSerializer):
    imovel = ImovelOutputSerializer()
    
    class Meta:
        model = Anuncio
        fields = '__all__'

class AnuncioInputSerializer(serializers.Serializer):
    imovel = serializers.UUIDField()
    nome_plataforma = serializers.CharField()
    taxa_plataforma = serializers.FloatField()

class AnuncioUpdateSerializer(serializers.Serializer):
    imovel = serializers.UUIDField(required=False)
    nome_plataforma = serializers.CharField(required=False)
    taxa_plataforma = serializers.FloatField(required=False)