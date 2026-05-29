import datetime
import typing


class HtmlParser(typing.Protocol):
    def parse_pages_urls(self, contents: str) -> dict[datetime.date, str]: ...
    def parse_pdfs_urls(self, contents: str) -> list[str]: ...
