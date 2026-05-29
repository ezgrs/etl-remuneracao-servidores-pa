import typing

from etl.domain.entities.registro import Registro


class PdfParser(typing.Protocol):
    def parse(self, contents: bytes) -> list[Registro]: ...
