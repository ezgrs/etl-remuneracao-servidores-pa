import datetime
import typing

from etl.domain.entities.registro import Registro


class Exporter(typing.Protocol):
    async def set_up(self) -> None: ...
    async def tear_down(self) -> None: ...

    async def write(self, date: datetime.date, record: Registro) -> None: ...
