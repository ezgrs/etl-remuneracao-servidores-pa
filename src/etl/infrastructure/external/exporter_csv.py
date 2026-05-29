from datetime import date

from etl.application.ports.exporter import Exporter
from etl.domain.entities.registro import Registro


class CsvExporter(Exporter):
    async def write(self, date: date, records: list[Registro]) -> None:
        return
