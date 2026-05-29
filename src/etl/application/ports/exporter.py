import datetime
import typing

from etl.domain.entities.registro import Registro


class Exporter(typing.Protocol):
    async def write(
        self, date: datetime.date, records: list[Registro]
    ) -> None: ...
