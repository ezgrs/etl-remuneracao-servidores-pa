import csv
import io
import pprint
import re
import typing

import pypdf

from etl.application.ports.pdf_parser import PdfParser
from etl.domain.entities.registro import Registro


class PyPdfPdfParser(PdfParser):
    departments: typing.Iterable[str]

    def __init__(self, *, departments: typing.Iterable[str]) -> None:
        self.departments = departments

    def parse(self, contents: bytes) -> list[Registro]:
        arg0_text = '|'.join(re.escape(department) for department in sorted(self.departments))
        row_pattern = re.compile(fr'^({arg0_text}) ([A-Z0\' ]+?) (Com Vínculo|Sem Vínculo) ([A-ZÇÉÊÃÕÚe \/\-0-9.,]+?) ([\(\)0-9.,]+)')

        reader = pypdf.PdfReader(io.BytesIO(contents))
        for page in reader.pages:
            groups: dict[float, list[tuple[float, str]]] = {}

            def visitor_text(
                text: str,
                cm: list[float],
                tm: list[float],
                font_dict: dict[str, typing.Any],
                font_size: float,
            ) -> None:
                _, _, _, _, x, y = tm
                y = y or (max(groups.keys()) if groups else 0)
                groups.setdefault(y, []).append((x, text))

            page.extract_text(visitor_text=visitor_text)
            for _, items in groups.items():
                value = ' '.join(value for item in items if (value := item[1].strip()))
                match value:
                    case '':
                        continue
                    case 'GOVERNO DO ESTADO DO PARÁ':
                        continue
                    case 'SECRETARIA DE ESTADO DE PLANEJAMENTO E ADMINISTRAÇÃO':
                        continue
                    case 'DEMONSTRATIVO DE REMUNERAÇÃO DE PESSOAL - PODER EXECUTIVO':
                        continue
                    case str() if value.startswith("Fonte: SIGIRH/") : # 'Fonte: SIGIRH/XXXXXX de XXXX - Parte X/X - V.X'
                        continue
                    case 'Órgão Nome Vínculo Cargo/Função Retroativos Férias':
                        continue
                    case 'Remuneração Adiantamento Aux Aliment Redutor Imposto de Renda Outros Valor':
                        continue
                    case 'Base 13º Salário Aux Transp Constitucional Previdência Descontos Líquido':
                        continue

                assert row_pattern.match(value), f"invalid header ({value=})"

        return []
