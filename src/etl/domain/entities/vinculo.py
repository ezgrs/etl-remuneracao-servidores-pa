import dataclasses

from etl.domain.value_objects.tipo_vinculo import TipoVinculo


@dataclasses.dataclass(kw_only=True, frozen=True)
class Vinculo:
    orgao: str
    ocupacao: str
    tipo: TipoVinculo
