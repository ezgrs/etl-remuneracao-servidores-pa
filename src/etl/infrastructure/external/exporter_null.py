import datetime

from etl.application.ports.exporter import Exporter
from etl.domain.entities.registro import Registro


class NullExporter(Exporter):
    async def write(
        self,
        date: datetime.date,
        records: list[Registro],
    ) -> None:
        return
