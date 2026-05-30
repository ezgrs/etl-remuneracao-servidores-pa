import datetime

import aiopath
import aiocsv

from etl.application.ports.exporter import Exporter
from etl.domain.entities.registro import Registro
from etl.domain.value_objects.tipo_vinculo import TipoVinculo


class CsvExporter(Exporter):
    path: aiopath.AsyncPath

    def __init__(self, *, path: aiopath.AsyncPath):
        self.path = path

    async def write(
        self,
        date: datetime.date,
        records: list[Registro],
    ) -> None:
        async with self.path.open("a", encoding="utf-8", newline="") as f:
            writer = aiocsv.AsyncWriter(f, delimiter=";")
            await writer.writerows(
                [
                    [
                        date.strftime("%m/%Y"),
                        record.vinculo.orgao,
                        record.servidor.nome,
                        {
                            TipoVinculo.EMPREGATICIO: "Com vínculo",
                            TipoVinculo.NAO_EMPREGATICIO: "Sem vínculo",
                        }[record.vinculo.tipo],
                        record.vinculo.ocupacao,
                        record.remuneracao.valor_bruto,
                        record.remuneracao.valor_liquido,
                    ]
                    for record in records
                ]
            )
