import asyncio
import datetime
import typing

import aiopath
import asyncclick as click
import httpx

from etl.application.ports.exporter import Exporter
from etl.application.ports.html_parser import HtmlParser
from etl.application.ports.pdf_parser import PdfParser
from etl.application.use_cases import crawl, load_canonical_departments
from etl.application.use_cases.downloaders.cached import CachedDownloader
from etl.application.use_cases.downloaders.delayed import DelayedDownloader
from etl.infrastructure.external.downloader_httpx import HttpxDownloader
from etl.infrastructure.external.exporter_csv import CsvExporter
from etl.infrastructure.external.exporter_null import NullExporter
from etl.infrastructure.external.html_parser_bs4 import Bs4HtmlParser
from etl.infrastructure.external.pdf_parser_pypdf import PyPdfPdfParser


class ObjectType[T](click.ParamType):
    name = "object"

    def __init__(self, mapping: dict[str, T]):
        self.mapping = mapping

    @typing.override
    def convert(
        self,
        value: str,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ):
        try:
            return self.mapping[value]
        except KeyError:
            self.fail(
                f"invalid choice: {value}. "
                f"Choose from: {', '.join(self.mapping)}",
                param,
                ctx,
            )

    @typing.override
    def get_metavar(self, param: click.Parameter, ctx: click.Context):
        return f"[{'|'.join(self.mapping)}]"


@click.command()
@click.option(
    "--delay",
    default=1,
    type=int,
    show_default=True,
    help="Delay between requests (in seconds).",
)
@click.option(
    "--format",
    "exporter_type",
    type=click.Choice(["csv"]),
    default="csv",
    show_default=True,
    help="Output format.",
)
@click.option(
    "--output-dir",
    type=click.Path(
        path_type=aiopath.AsyncPath, file_okay=False, dir_okay=True
    ),
    default=None,
    help="Output directory.",
)
@click.option(
    "--cache-dir",
    type=click.Path(
        path_type=aiopath.AsyncPath, file_okay=False, dir_okay=True
    ),
    default=None,
    help="Cache directory.",
)
@click.option(
    "--html-parser",
    type=ObjectType({"bs4": Bs4HtmlParser()}),
    default="bs4",
    show_default=True,
    help="HTML parser to use.",
)
@click.option(
    "--pdf-parser",
    "pdf_parser_type",
    type=click.Choice(["pypdf"]),
    default="pypdf",
    show_default=True,
    help="PDF parser to use.",
)
async def main(
    delay: int,
    cache_dir: aiopath.AsyncPath | None,
    output_dir: aiopath.AsyncPath | None,
    html_parser: HtmlParser,
    pdf_parser_type: typing.Literal["pypdf"],
    exporter_type: typing.Literal["csv"],
) -> None:
    exporter: Exporter
    if output_dir is None:
        exporter = NullExporter()
    else:
        match exporter_type:
            case "csv":
                exporter = CsvExporter(path=output_dir / "output.csv")

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=None,
        verify=False,
    ) as client:
        downloader = HttpxDownloader(client)
        downloader = DelayedDownloader(
            downloader,
            delay=datetime.timedelta(seconds=delay),
        )
        if cache_dir is not None:
            downloader = CachedDownloader(
                downloader,
                path=cache_dir,
            )

        pdf_parser: PdfParser
        match pdf_parser_type:
            case "pypdf":
                pdf_parser = PyPdfPdfParser(
                    departments=await load_canonical_departments(
                        downloader=downloader
                    )
                )

        await crawl(
            downloader=downloader,
            html_parser=html_parser,
            pdf_parser=pdf_parser,
            exporter=exporter,
        )


if __name__ == "__main__":
    asyncio.run(main())
