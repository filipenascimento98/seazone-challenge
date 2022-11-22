from datetime import datetime
from api.domain.base import DomainBase
from api.data_access.imovel import ImovelRepository


class ImovelDomain(DomainBase):
    def __init__(self):
        super().__init__(ImovelRepository())
    
    def criar(self, dados):
        data_ativacao = datetime.strptime(dados['data_ativacao'], "%d/%m/%Y")

        try:
            dados['data_ativacao'] = data_ativacao.strftime("%Y-%m-%d")
            ret = self.repository.criar(dados)
            self.repository.salvar(ret)
        except Exception as e:
            return ("Não foi possível adicionar o objeto a base de dados.", 500)
        
        return {"message": ret.pk, "status": 201}

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