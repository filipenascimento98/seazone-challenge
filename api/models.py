from uuid import uuid4

from django.db import models


class ComumInfo(models.Model):
    data_criacao = models.DateTimeField("Data de criação", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Data de atualização", auto_now=True)

    class Meta:
        abastract = True

class Imovel(ComumInfo):
    cd_imovel = models.UUIDField(primary_key=True, default=uuid4)
    limite_hospedes = models.PositiveIntegerField("Limite de hóspedes")
    qtd_banheiro = models.PositiveIntegerField("Quantidade de banheiros")
    permitido_animais = models.BooleanField("Permitido animais de estimação")
    valor_limpeza = models.FloatField("Valor da limpeza")
    data_ativacao = models.DateField("Data de ativação")

    class Meta:
        verbose_name = "Imóvel"
        verbose_name_plural = "Imóveis"

class Anuncio(ComumInfo):
    imovel = models.ForeignKey(
        "Imovel",
        verbose_name="Imóvel",
        related_name="anuncio",
        on_delete=models.CASCADE,
        primary_key=True
    )
    nome_plataforma = models.CharField("Nome da plataforma", max_length=200)
    taxa_plataforma = models.FloatField("Taxa da plataforma")

    class Meta:
        verbose_name = "Anúncio"
        verbose_name_plural = "Anúncios"

class Reserva(ComumInfo):
    cd_reserva = models.UUIDField(primary_key=True, default=uuid4)
    anuncio = models.ForeignKey(
        "Anuncio",
        verbose_name="Anúncio",
        related_name="reserva",
        on_delete=models.CASCADE,
    )
    data_check_in = models.DateField("Check-in")
    data_check_out = models.DateField("Check-out")
    preco_total = models.FloatField("Preço total")
    comentario = models.TextField("Comentário")
    num_hospedes = models.PositiveIntegerField("Número de hóspedes")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"