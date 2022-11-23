from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.data_access.reserva import ReservaRepository

class ReservaTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.reserva_repo = ReservaRepository()

        self.imovel_obj = {
            "limite_hospedes": 50,
            "qtd_banheiro": 30,
            "permitido_animais": True,
            "valor_limpeza": 120,
            "data_ativacao": "01/01/2022"
        }
        response_imovel = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')

        self.anuncio_obj = {
            "imovel": response_imovel.data["message"],
            "nome_plataforma": 'AisBnb',
            "taxa_plataforma": 10.50
        }
        response_anuncio = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')

        self.reserva_obj = {
            "anuncio": response_anuncio.data["message"],
            "data_check_in": "01/02/2022",
            "data_check_out": "05/02/2022",
            "preco_total": 150,
            "comentario": "Lorem Ipsum",
            "num_hospedes": 20
        }
    
    def test_create_reserva(self):
        """
        POST - Cria uma reserva
        """
        response = self.api_client.post(reverse('reserva-list'), self.reserva_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se a reserva está na base de dados
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], self.reserva_repo.obter({'cd_reserva': response.data["message"]}).cd_reserva)
    
    def test_check_in_invalid(self):
        """
        POST - Tenta criar uma reserva check-in inválido
        """
        self.reserva_obj['data_check_in'] = '06/02/2022' # Sendo que check-out é 05/02/2022
        response = self.api_client.post(reverse('reserva-list'), self.reserva_obj, format='json')

        # Verifico:
        # - Se o status é 400
        # - Se o retorno é igual a mensagem "A data de check-out deve ser posterior a data de data_check_in"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "A data de check-out deve ser posterior a data de data_check_in")
    
    def test_list_reserva(self):
        """
        GET - Lista todas reservas
        """
        response_post = self.api_client.post(reverse('reserva-list'), self.reserva_obj, format='json')
        response_get = self.api_client.get(reverse('reserva-list'), format='json')

        # Verifico:
        # - Se o status é 201
        # - Se a reserva está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["message"], self.reserva_repo.obter({'cd_reserva': response_post.data["message"]}).cd_reserva)

        # Verifico:
        # - Se o status é 200
        # - Se a quantidade de reservas retornada é igual a quantidade registrada na base
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), len(self.reserva_repo.listar()))
    
    def test_retrieve_reserva(self):
        """
        GET - Retorna uma reserva específica
        """
        response_post = self.api_client.post(reverse('reserva-list'), self.reserva_obj, format='json')
        response_get = self.api_client.get(reverse('reserva-detail', args=[str(response_post.data['message'])]), format='json')

        # Verifico:
        # - Se o status é 201
        # - Se a reserva está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["message"], self.reserva_repo.obter({'cd_reserva': response_post.data["message"]}).cd_reserva)

        # Verifico:
        # - Se o status é 201
        # - Se a reserva recuperado está na base
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data['cd_reserva'],
                         str(self.reserva_repo.obter({'cd_reserva': response_post.data["message"]}).cd_reserva))
    
    def test_destroy_reserva(self):
        """
        DELETE - Deleta uma reserva
        """
        response_post = self.api_client.post(reverse('reserva-list'), self.reserva_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se a reserva está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.reserva_repo.obter({'cd_reserva': response_post.data["message"]}).cd_reserva)

        response_delete = self.api_client.delete(reverse('reserva-detail', args=[str(response_post.data['message'])]), format='json')

        # Verifico:
        # - Se o status é 204
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_metodos_nao_permitidos(self):
        """
        PUT e PATCH - Tenta disparar esses dois métodos não permitidos
        """
        response_post = self.api_client.post(reverse('reserva-list'), self.reserva_obj, format='json')
        self.reserva_obj['preco_total'] = 500
        response_put = self.api_client.put(reverse('reserva-detail', args=[str(response_post.data['message'])]),
                                           self.reserva_obj, format='json')
        response_patch = self.api_client.patch(reverse('reserva-detail', args=[str(response_post.data['message'])]),
                                           self.reserva_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se a reserva está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.reserva_repo.obter({'cd_reserva': response_post.data["message"]}).cd_reserva)

        # Verifico:
        # - Se o status é 405 para o PUT e para o PATCH
        # - Se a alteração foi registrada na base
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
