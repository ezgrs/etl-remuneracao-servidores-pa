import datetime
import typing


class PdfParser(typing.Protocol):
    async def parse(self, date: datetime.date, contents: bytes) -> None: ...
