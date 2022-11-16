from api.data_access.base import RepositoryBase
from api.models import Reserva


class ReservaRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Reserva)