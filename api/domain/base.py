from django.core.exceptions import ObjectDoesNotExist


class DomainBase:
    def __init__(self, repository):
        self.repository = repository

    def listar(self):
        try:
            ret = self.repository.listar()
        except ObjectDoesNotExist as e:
            return ("Objeto não encontrado", 404)
        
        return {"message": ret, "status": 200}
    
    def obter(self, pk):
        try:
            query_params={"pk": pk}
            ret = self.repository.obter(query_params=query_params)
        except ObjectDoesNotExist as e:
            return ("Objeto não encontrado", 404)
        
        return {"message": ret, "status": 200}
    
    def criar(self, dados):
        try:
            ret = self.repository.criar(dados)
            self.repository.salvar(ret)
        except Exception as e:
            return ("Não foi possível adicionar o objeto a base de dados.", 500)
        
        return {"message": ret.pk, "status": 201}
    
    def excluir(self, pk):
        try:
            query_params={"pk": pk}
            ret = self.repository.obter(query_params=query_params)
        except ObjectDoesNotExist as e:
            return ("Objeto não encontrado", 404)
        try:
            self.repository.excluir(ret)
        except Exception as e:
            return ("Não foi possível excluir o objeto da base de dados.", 500)
        
        return {"message": "Objeto excluído", "status": 204}