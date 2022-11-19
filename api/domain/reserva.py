import logging
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from api.domain.base import DomainBase
from api.data_access.reserva import ReservaRepository
from api.data_access.anuncio import AnuncioRepository


class ReservaDomain(DomainBase):
    def __init__(self):
        self.anuncio_repository = AnuncioRepository()
        super().__init__(ReservaRepository())
    
    def criar(self, dados):
        data_check_in = datetime.strptime(dados['data_check_in'], "%d/%m/%Y")
        data_check_out = datetime.strptime(dados['data_check_out'], "%d/%m/%Y")

        if data_check_in >= data_check_out:
            return ("A data de check-out deve ser posterior a data de data_check_in", 400)

        try:
            query_params = {"cd_anuncio": dados['anuncio']}
            anuncio = self.anuncio_repository.obter(query_params=query_params)
            dados['anuncio'] = anuncio
        except ObjectDoesNotExist as e:
            logging.error(e)
            return ("Anúncio não encontrado", 404)
        
        try:
            ret = self.repository.criar(dados)
            self.repository.salvar(ret)
        except Exception as e:
            logging.error(e)
            return ("Não foi possível adicionar o objeto a base de dados", 500)
        
        return {"message": ret.pk, "status": 201}