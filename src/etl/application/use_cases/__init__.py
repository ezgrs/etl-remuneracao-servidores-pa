import datetime

from etl.application.ports.downloader import Downloader
from etl.application.ports.exporter import Exporter
from etl.application.ports.html_parser import HtmlParser
from etl.application.ports.pdf_parser import PdfParser


async def crawl(
    *,
    downloader: Downloader,
    html_parser: HtmlParser,
    pdf_parser: PdfParser,
    exporter: Exporter,
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
        for pdf_url in pdfs_urls:
            try:
                pdf_contents = await downloader.download_file(
                    pdf_url.replace("http://", "https://")
                )
            except Exception:
                continue

            records = pdf_parser.parse(pdf_contents)
            await exporter.write(date, records)
