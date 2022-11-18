from api.domain.base import DomainBase
from api.data_access.imovel import ImovelRepository


class ImovelDomain(DomainBase):
    def __init__(self):
        super().__init__(ImovelRepository())

    def atualizar(self, pk, dados):
        try:
            query_params = {"pk": pk}
            imovel = self.repository.obter(query_params=query_params)
        except Exception as e:
            return {"message": "Não foi possível atualizar o objeto a base de dados.", "status": 400}
        
        imovel.limite_hospedes = dados['limite_hospedes']
        imovel.qtd_banheiro = dados['qtd_banheiro']
        imovel.permitido_animais = dados['permitido_animais']
        imovel.valor_limpeza = dados['valor_limpeza']
        imovel.data_ativacao = dados['data_ativacao']

        imovel.save()
        
        return {"message": "Objeto alterado", "status": 200}