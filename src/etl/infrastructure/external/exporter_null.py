import datetime

from etl.application.ports.exporter import Exporter
from etl.domain.entities.registro import Registro


class NullExporter(Exporter):
    async def set_up(self) -> None:
        return

    async def tear_down(self) -> None:
        return

    async def write(
        self,
        date: datetime.date,
        record: Registro,
    ) -> None:
        return
