class RepositoryBase:
    def __init__(self, model):
        self.model = model
    
    def criar(self, obj):
        '''
        Realiza a criação de um model
        Args:
        - obj: Dicionário com os campos do model
        Returns:
        - obj: Instância do objeto(model) criado
        '''
        return self.model(**obj)
        
    def salvar(self, obj):
        '''
        Realiza a inserção de um model na base de dados
        Args:
        - obj: Objeto(model) criado porém ainda não salvo
        '''
        obj.save()
    
    def obter(self, query_params={}, select_related=[]):
        '''
        Retorna um único objeto com base nos parâmetros definidos:
        Args:
            - query_params: Dicionário com os valores referentes a filtragem
            da consulta no ORM.
            - select_related: Lista de strings com os campos a serem chamados
            no select related da consulta.
        Returns:
            - obj: Objeto.
        '''
        return self.model.objects.select_related(*select_related).get(**query_params)
    
    def obter_com_referenciados(self, query_params={}, prefetch_related=[]):
        '''
        Retorna um único objeto com base nos parâmetros definidos e seus campos que referenciam
        outros models, caso passe o prefetch_related:
        Args:
            - query_params: Dicionário com os valores referentes a filtragem
            da consulta no ORM.
            - prefetch_related: Lista de strings com os campos a serem chamados
            no prefetch related da consulta.
        Returns:
            - obj: Objeto.
        '''
        return self.model.objects.prefetch_related(*prefetch_related).get(**query_params)

    def listar(self):
        '''
        Realiza a listagem de dados.
            Returns:
            - Lista de objetos.
        '''
        return self.model.objects.all()
    
    def atualizar(self, obj, dados_alterados=[]):
        """
        Realiza a alteração parcial dos campos de um objeto via ORM.
        Args:
        - obj: Objeto com as alterações.
        - dados_alterados: Dicionário com o campo update_fields e o seu 
        valor sendo uma lista indicando os campos alterados
        Returns:
        - obj: Objeto alterado.
        """
        return obj.save(update_fields=dados_alterados)
    
    def excluir(self, obj):
        """
        Realiza a exclusão de um objeto via ORM.
        Args:
        - obj: Objeto a ser excluído
        Returns:
        - Não há retorno
        """
        return obj.delete()