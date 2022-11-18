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
            return {"message": "Objeto não encontrado", "status": 400}
        
        imovel.limite_hospedes = dados.get('limite_hospedes', imovel.limite_hospedes)
        imovel.qtd_banheiro = dados.get('qtd_banheiro', imovel.qtd_banheiro)
        imovel.permitido_animais = dados.get('permitido_animais', imovel.permitido_animais)
        imovel.valor_limpeza = dados.get('valor_limpeza', imovel.valor_limpeza)
        imovel.data_ativacao = dados.get('data_ativacao', imovel.data_ativacao)

        campos_alterados = []
        for key in dados:
            campos_alterados.append(key)

        self.repository.atualizar(imovel, campos_alterados)
        
        return {"message": "Objeto alterado", "status": 200}