import dataclasses
import decimal


@dataclasses.dataclass(kw_only=True, frozen=True)
class Remuneracao:
    base: decimal.Decimal

    adiantamento_13_salario: decimal.Decimal
    retroativos: decimal.Decimal
    ferias: decimal.Decimal
    auxilios: decimal.Decimal
    redutor_constitucional: decimal.Decimal
    imposto_de_renda: decimal.Decimal
    outros_descontos: decimal.Decimal
    valor_liquido: decimal.Decimal
