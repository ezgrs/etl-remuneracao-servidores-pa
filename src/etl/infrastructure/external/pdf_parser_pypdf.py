import io
import typing

import pypdf

from etl.application.ports.pdf_parser import PdfParser
from etl.domain.entities.registro import Registro


class PyPdfPdfParser(PdfParser):
    def parse(self, contents: bytes) -> list[Registro]:
        reader = pypdf.PdfReader(io.BytesIO(contents))
        for page in reader.pages:
            groups: dict[float, dict[str, list[str]]] = {}

            def visitor_body(
                text: str,
                cm: list[float],
                tm: list[float],
                font_dict: dict[str, typing.Any],
                font_size: float,
            ):
                _, _, _, _, x, y = tm
                groups.setdefault(y, {}).setdefault(
                    f"{round(x, 2)}", []
                ).append(text)

            page.extract_text(visitor_text=visitor_body)
            is_header = True
            for _, row_groups in groups.items():
                tokens = [
                    (x, "".join(texts)) for x, texts in row_groups.items()
                ]
                if is_header:
                    if tokens[0][1] == "Base":
                        is_header = False
                    continue

                if tokens[0][1] == "GOVERNO DO ESTADO DO PARÁ":
                    break

                print(tokens)
                assert tokens[0][0] == "24.8"

        return []
