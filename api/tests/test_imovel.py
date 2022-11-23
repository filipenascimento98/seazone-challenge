from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.data_access.imovel import ImovelRepository
from api.domain.imovel import ImovelDomain

class ImovelTest(TestCase):
    
    def setUp(self):
        self.api_client = APIClient()
        self.imovel_repo = ImovelRepository()
        self.imovel_domain = ImovelDomain()

        self.imovel_obj = {
            "limite_hospedes": 50,
            "qtd_banheiro": 30,
            "permitido_animais": True,
            "valor_limpeza": 120,
            "data_ativacao": "01/01/2022"
        }
    
    def test_create_imovel(self):
        """
        POST - Cria um imóvel
        """
        response = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel está na base de dados
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], self.imovel_repo.obter({'cd_imovel': response.data["message"]}).cd_imovel)
    
    def test_create_data_ativacao_invalida(self):
        """
        POST - Tenta criar um imóvel com a data de ativação posterior a data atual
        """
        self.imovel_obj['data_ativacao'] = '25/12/2100'
        response = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')

        # Verifico:
        # - Se o status é 422
        # - Se o a mensagem de retorno é "A data de ativação não pode ser posterior a data atual"
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data['message'], "A data de ativação não pode ser posterior a data atual")
    
    def test_list_imovel(self):
        """
        GET - Lista todos imóveis
        """
        response_post = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')
        response_get = self.api_client.get(reverse('imovel-list'), format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["message"], self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).cd_imovel)

        # Verifico:
        # - Se o status é 200
        # - Se a quantidade de imóveis retornada é igual a quantidade registrada na base
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), len(self.imovel_repo.listar()))
    
    def test_retrieve_imovel(self):
        """
        GET - Retorna um imóvel específico
        """
        response_post = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')
        response_get = self.api_client.get(reverse('imovel-detail', args=[str(response_post.data['message'])]), format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["message"], self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).cd_imovel)

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel recuperado está na base
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data['cd_imovel'],
                         str(self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).cd_imovel))
    
    def test_update_imovel(self):
        """
        PUT - Atualiza um imóvel
        """
        response_post = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')
        self.imovel_obj['limite_hospedes'] = 100
        response_put = self.api_client.put(reverse('imovel-detail', args=[str(response_post.data['message'])]),
                                           self.imovel_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).cd_imovel)

        # Verifico:
        # - Se o status é 200
        # - Se a alteração foi registrada na base
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.assertEqual(self.imovel_obj['limite_hospedes'],
                         self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).limite_hospedes)
    
    def test_partial_update_imovel(self):
        """
        PUT - Atualiza parcialmente um imóvel
        """
        response_post = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')
        self.imovel_obj['limite_hospedes'] = 100
        response_patch = self.api_client.patch(reverse('imovel-detail', args=[str(response_post.data['message'])]),
                                           self.imovel_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).cd_imovel)

        # Verifico:
        # - Se o status é 200
        # - Se a alteração foi registrada na base
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(self.imovel_obj['limite_hospedes'],
                         self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).limite_hospedes)
    
    def test_destroy_imovel(self):
        """
        DELETE - Testa a exclusão de um imóvel
        """
        response_post = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o imóvel está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.imovel_repo.obter({'cd_imovel': response_post.data["message"]}).cd_imovel)

        response_delete = self.api_client.delete(reverse('imovel-detail', args=[str(response_post.data['message'])]), format='json')

        # Verifico:
        # - Se o status é 204
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)