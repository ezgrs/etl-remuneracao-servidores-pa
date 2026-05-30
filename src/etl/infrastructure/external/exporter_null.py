import csv
import datetime
import io

import aiopath

from etl.application.ports.exporter import Exporter
from etl.domain.entities.registro import Registro
from etl.domain.value_objects.tipo_vinculo import TipoVinculo


class NullExporter(Exporter):
    async def write(
        self,
        date: datetime.date,
        records: list[Registro],
    ) -> None:
        return
