from rest_framework import serializers
from api.models import Reserva
from api.serializers.anuncio import AnuncioOutputSerializer


class ReservaOutputSerializer(serializers.ModelSerializer):
    anuncio = AnuncioOutputSerializer()

    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaInputSerializer(serializers.Serializer):
    anuncio = serializers.UUIDField()
    data_check_in = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    data_check_out = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y"])
    preco_total = serializers.FloatField()
    comentario = serializers.CharField()
    num_hospedes = serializers.IntegerField()