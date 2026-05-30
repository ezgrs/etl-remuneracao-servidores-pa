import asyncio
import contextlib
import datetime

import aiopath
import aiocsv
import aiocsv.protocols

from etl.application.ports.exporter import Exporter
from etl.domain.entities.registro import Registro
from etl.domain.enums.tipo_vinculo import TipoVinculo


class CsvExporter(Exporter):
    path: aiopath.AsyncPath

    writer: aiocsv.AsyncWriter | None
    exit_stack: contextlib.AsyncExitStack

    def __init__(self, *, path: aiopath.AsyncPath):
        self.path = path

        self.writer = None
        self.exit_stack = contextlib.AsyncExitStack()

    async def set_up(self) -> None:
        file = await self.exit_stack.enter_async_context(
            self.path.open("w+", encoding="utf-8", newline="")
        )
        self.writer = aiocsv.AsyncWriter(file, delimiter=";")

    async def tear_down(self) -> None:
        await self.exit_stack.aclose()
        self.writer = None

    async def write(
        self,
        date: datetime.date,
        record: Registro,
    ) -> None:
        writer = self.writer
        if writer is None:
            return
        await writer.writerow(
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
        )
