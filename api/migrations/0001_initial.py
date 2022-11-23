# Generated by Django 4.1.3 on 2022-11-18 23:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('cd_imovel', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('nome_plataforma', models.CharField(max_length=200, verbose_name='Nome da plataforma')),
                ('taxa_plataforma', models.FloatField(verbose_name='Taxa da plataforma')),
            ],
            options={
                'verbose_name': 'Anúncio',
                'verbose_name_plural': 'Anúncios',
            },
        ),
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('cd_imovel', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('limite_hospedes', models.PositiveIntegerField(verbose_name='Limite de hóspedes')),
                ('qtd_banheiro', models.PositiveIntegerField(verbose_name='Quantidade de banheiros')),
                ('permitido_animais', models.BooleanField(verbose_name='Permitido animais de estimação')),
                ('valor_limpeza', models.FloatField(verbose_name='Valor da limpeza')),
                ('data_ativacao', models.DateField(verbose_name='Data de ativação')),
            ],
            options={
                'verbose_name': 'Imóvel',
                'verbose_name_plural': 'Imóveis',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('cd_reserva', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('data_check_in', models.DateField(verbose_name='Check-in')),
                ('data_check_out', models.DateField(verbose_name='Check-out')),
                ('preco_total', models.FloatField(verbose_name='Preço total')),
                ('comentario', models.TextField(verbose_name='Comentário')),
                ('num_hospedes', models.PositiveIntegerField(verbose_name='Número de hóspedes')),
                ('anuncio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserva', to='api.anuncio', verbose_name='Anúncio')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.AddField(
            model_name='anuncio',
            name='imovel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anuncio', to='api.imovel', verbose_name='Imóvel'),
        ),
    ]
