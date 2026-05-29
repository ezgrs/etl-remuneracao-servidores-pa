import dataclasses

from etl.domain.entities.servidor import Servidor
from etl.domain.entities.vinculo import Vinculo
from etl.domain.entities.remuneracao import Remuneracao


@dataclasses.dataclass(kw_only=True, frozen=True)
class Registro:
    servidor: Servidor
    vinculo: Vinculo
    remuneracao: Remuneracao
