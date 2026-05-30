import dataclasses
import decimal


@dataclasses.dataclass(kw_only=True, frozen=True)
class Remuneracao:
    valor_bruto: decimal.Decimal
    valor_liquido: decimal.Decimal
