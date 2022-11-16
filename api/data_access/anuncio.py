from api.data_access.base import RepositoryBase
from api.models import Anuncio


class AnuncioRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Anuncio)