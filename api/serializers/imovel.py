from rest_framework import serializers
from api.models import Imovel
from api.domain.imovel import ImovelDomain


class ImovelOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = '__all__'

class ImovelInputSerializer(serializers.Serializer):
    limite_hospedes = serializers.IntegerField()
    qtd_banheiro = serializers.IntegerField()
    permitido_animais = serializers.BooleanField()
    valor_limpeza = serializers.FloatField()
    data_ativacao = serializers.DateField()