import dataclasses

from etl.domain.enums.tipo_vinculo import TipoVinculo


@dataclasses.dataclass(kw_only=True, frozen=True)
class Vinculo:
    orgao: str
    ocupacao: str
    tipo: TipoVinculo
