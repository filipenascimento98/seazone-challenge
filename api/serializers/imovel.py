from rest_framework import serializers
from api.models import Imovel


class ImovelOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = '__all__'

class ImovelInputSerializer(serializers.Serializer):
    limite_hospedes = serializers.IntegerField()
    qtd_banheiro = serializers.IntegerField()
    permitido_animais = serializers.BooleanField()
    valor_limpeza = serializers.FloatField()
    data_ativacao = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])

class ImovelUpdateSerializer(serializers.Serializer):
    limite_hospedes = serializers.IntegerField(required=False)
    qtd_banheiro = serializers.IntegerField(required=False)
    permitido_animais = serializers.BooleanField(required=False)
    valor_limpeza = serializers.FloatField(required=False)
    data_ativacao = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"], required=False)