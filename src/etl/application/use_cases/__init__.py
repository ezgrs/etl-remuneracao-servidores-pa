import asyncio
import datetime
import typing

from etl.application.ports.downloader import Downloader
from etl.application.ports.html_parser import HtmlParser
from etl.application.ports.pdf_parser import PdfParser


async def _parse_pdf(
    date: datetime.date,
    url: str,
    *,
    downloader: Downloader,
    pdf_parser: PdfParser,
) -> None:
    try:
        pdf_contents = await downloader.download_file(
            url.replace("http://", "https://")
        )
    except Exception:
        return

    await pdf_parser.parse(date, pdf_contents)


async def crawl(
    *,
    downloader: Downloader,
    html_parser: HtmlParser,
    pdf_parser: PdfParser,
    url: str = "https://www.seplad.pa.gov.br/remuneracao-de-servidores/",
    min_date: datetime.date | None = None,
    max_date: datetime.date | None = None,
) -> None:
    main_page_html = await downloader.download_html(url)
    dates_urls_items = sorted(
        [
            (date, url)
            for date, url in html_parser.parse_pages_urls(
                main_page_html
            ).items()
            if (min_date is None or min_date <= date)
            and (max_date is None or date <= max_date)
        ],
        key=lambda item: item[0],
        reverse=True,
    )
    for date, date_url in dates_urls_items:
        date_page_html = await downloader.download_html(
            date_url.replace("http://", "https://")
        )
        pdfs_urls = html_parser.parse_pdfs_urls(date_page_html)
        await asyncio.gather(
            *(
                _parse_pdf(
                    date,
                    pdf_url,
                    downloader=downloader,
                    pdf_parser=pdf_parser,
                )
                for pdf_url in pdfs_urls
            )
        )


async def load_canonical_departments(
    *,
    downloader: Downloader,
    url: str = "https://ptp-api-dados.sistemas.pa.gov.br/organizacoes/superiores",
) -> typing.Iterable[str]:
    records = await downloader.download_json(url)
    mapping = {
        # API -> SIGIRH
        "SEJU": "SEJUDH",
        "SEOP": "SEDOP",
        "PCPA": "PC",
        "IOEPA": "IOE",
        "IMETROPARÁ": "IMETROPARA",
        "IGEPPS": "IGEPREV",
        "IDEFLOR-BIO": "IDEFLORBIO",
        "GABVICE": "GAB/VICE",
        "FSCMPA": "FSCMP",
        "FPARÁPAZ": "FPROPAZ",
        "DETRAN/PA": "DETRAN",
        "CBM/PA": "CBM",
        "CASA MILITAR": "CASA MILIT",
        "ADEPARÁ": "ADEPARA",
    }
    siglas = [record["sigla"] for record in records]
    siglas = [mapping.get(sigla, sigla) for sigla in siglas]
    siglas = [*siglas, "NGPM", "PME", "ENCARGOS", "DEF. PUB."]
    return siglas
