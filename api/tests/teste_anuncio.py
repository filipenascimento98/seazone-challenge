from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.data_access.anuncio import AnuncioRepository


class AnuncioTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.anuncio_repo = AnuncioRepository()

        self.imovel_obj = {
            "limite_hospedes": 50,
            "qtd_banheiro": 30,
            "permitido_animais": True,
            "valor_limpeza": 120,
            "data_ativacao": "01/01/2022"
        }
        response = self.api_client.post(reverse('imovel-list'), self.imovel_obj, format='json')

        self.anuncio_obj = {
            "imovel": response.data["message"],
            "nome_plataforma": 'AisBnb',
            "taxa_plataforma": 10.50
        }
    
    def test_create_anuncio(self):
        """
        POST - Cria um anúncio
        """
        response = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], self.anuncio_repo.obter({'cd_anuncio': response.data["message"]}).cd_anuncio)
    
    def test_create_anuncio_com_imovel_invalido(self):
        """
        POST - Tenta criar um anúncio com um imóvel que não existe
        """
        self.anuncio_obj['imovel'] = '3c86cc6a-bec8-4258-8fee-928dadf79d9a'
        response = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Imóvel não encontrado")
    
    def test_list_anuncio(self):
        """
        GET - Lista todos anúncios
        """
        response_post = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')
        response_get = self.api_client.get(reverse('anuncio-list'), format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["message"], self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).cd_anuncio)

        # Verifico:
        # - Se o status é 200
        # - Se a quantidade de anúncios retornada é igual a quantidade registrada na base
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), len(self.anuncio_repo.listar()))
    
    def test_retrieve_anuncio(self):
        """
        GET - Retorna um anúncio específico
        """
        response_post = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')
        response_get = self.api_client.get(reverse('anuncio-detail', args=[str(response_post.data['message'])]), format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data["message"], self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).cd_anuncio)

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio recuperado está na base
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data['cd_anuncio'],
                         str(self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).cd_anuncio))
    
    def test_update_anuncio(self):
        """
        PUT - Atualiza um anúncio
        """
        response_post = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')
        self.anuncio_obj['nome_plataforma'] = 'Centro de Imóveis'
        response_put = self.api_client.put(reverse('anuncio-detail', args=[str(response_post.data['message'])]),
                                           self.anuncio_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).cd_anuncio)

        # Verifico:
        # - Se o status é 200
        # - Se a alteração foi registrada na base
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.assertEqual(self.anuncio_obj['nome_plataforma'],
                         self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).nome_plataforma)
    
    def test_partial_update_anuncio(self):
        """
        PATCH - Atualiza parcialmente um anúncio
        """
        response_post = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')
        self.anuncio_obj['nome_plataforma'] = 'Centro de Imóveis'
        response_patch = self.api_client.patch(reverse('anuncio-detail', args=[str(response_post.data['message'])]),
                                           self.anuncio_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).cd_anuncio)

        # Verifico:
        # - Se o status é 200
        # - Se a alteração foi registrada na base
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(self.anuncio_obj['nome_plataforma'],
                         self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).nome_plataforma)
    
    def test_metodo_nao_permitido(self):
        """
        DELETE - Tenta deletar um anúncio, porém esse método HTTP não é permitido
        """
        response_post = self.api_client.post(reverse('anuncio-list'), self.anuncio_obj, format='json')

        # Verifico:
        # - Se o status é 201
        # - Se o anúncio está na base de dados
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['message'], self.anuncio_repo.obter({'cd_anuncio': response_post.data["message"]}).cd_anuncio)

        response_delete = self.api_client.delete(reverse('anuncio-detail', args=[str(response_post.data['message'])]), format='json')

        # Verifico:
        # - Se o status é 405
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)