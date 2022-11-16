from api.data_access.repository_base import RepositoryBase
from api.models import Imovel


class ImovelRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Imovel)