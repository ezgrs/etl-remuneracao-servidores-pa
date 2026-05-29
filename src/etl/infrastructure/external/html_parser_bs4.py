import datetime

import bs4

from etl.application.ports.html_parser import HtmlParser


class Bs4HtmlParser(HtmlParser):
    def parse_pages_urls(self, contents: str) -> dict[datetime.date, str]:
        soup = bs4.BeautifulSoup(contents, features="html.parser")

        urls: dict[datetime.date, str] = {}

        year: int | None
        for year_panel_elem in soup.find_all("div", class_="vc_tta-panel"):
            year = None
            for month, month_text_elem in enumerate(
                year_panel_elem.find_all("a")
            ):
                text = month_text_elem.text
                if month > 12:
                    break
                if month == 0:
                    year = int(text)
                else:
                    assert year is not None, "year is None"
                    url = month_text_elem.get("href")
                    assert isinstance(url, str), f"url is not a str: {url}"
                    urls[datetime.date(year, month, 1)] = url

        return urls

    def parse_pdfs_urls(self, contents: str) -> list[str]:
        soup = bs4.BeautifulSoup(contents, features="html.parser")
        urls: list[str] = []
        for elem in soup.find_all("div", class_="wr-default-page"):
            for part_text_elem in elem.find_all("a"):
                url = part_text_elem.get("href")
                assert isinstance(url, str), f"url is not a str: {url}"
                urls.append(url)

        return urls
