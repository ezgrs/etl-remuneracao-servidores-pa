import dataclasses


@dataclasses.dataclass(kw_only=True, frozen=True)
class Servidor:
    nome: str
