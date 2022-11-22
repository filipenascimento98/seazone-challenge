import logging
from django.core.exceptions import ObjectDoesNotExist

from api.domain.base import DomainBase
from api.data_access.anuncio import AnuncioRepository
from api.data_access.imovel import ImovelRepository


class AnuncioDomain(DomainBase):
    def __init__(self):
        self.imovel_repository = ImovelRepository()
        super().__init__(AnuncioRepository())
    
    def criar(self, dados):
        try:
            query_params = {"cd_imovel": dados['imovel']}
            imovel = self.imovel_repository.obter(query_params=query_params)
            dados['imovel'] = imovel
        except ObjectDoesNotExist as e:
            logging.error(e)
            return ("Imóvel não encontrado", 404)
        
        try:
            ret = self.repository.criar(dados)
            self.repository.salvar(ret)
        except Exception as e:
            logging.error(e)
            return ("Não foi possível adicionar o objeto a base de dados", 500)
        
        return {"message": ret.pk, "status": 201}
    
    def atualizar(self, pk, dados):
        try:
            query_params = {"pk": pk}
            anuncio = self.repository.obter(query_params=query_params)
        except Exception as e:
            return ("Objeto não encontrado", 404)
        
        try:
            query_params = {"cd_imovel": dados.get('imovel', anuncio.imovel.pk)}
            imovel = self.imovel_repository.obter(query_params=query_params)
            anuncio.imovel = imovel
        except ObjectDoesNotExist as e:
            logging.error(e)
            return ("Imóvel não encontrado", 404)
        
        anuncio.nome_plataforma = dados.get('nome_plataforma', anuncio.nome_plataforma)
        anuncio.taxa_plataforma = dados.get('taxa_plataforma', anuncio.taxa_plataforma)

        campos_alterados = []
        for key in dados:
            campos_alterados.append(key)

        self.repository.atualizar(anuncio, campos_alterados)
        
        return {"message": "Objeto alterado", "status": 200}
