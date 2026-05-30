import asyncio
import datetime
import typing

from etl.application.ports.downloader import Downloader


class DelayedDownloader(Downloader):
    downloader: Downloader
    delay: datetime.timedelta

    def __init__(
        self, downloader: Downloader, *, delay: datetime.timedelta
    ) -> None:
        self.downloader = downloader
        self.delay = delay

    async def download_html(self, url: str) -> str:
        await asyncio.sleep(self.delay.total_seconds())
        return await self.downloader.download_html(url)

    async def download_file(self, url: str) -> bytes:
        await asyncio.sleep(self.delay.total_seconds())
        return await self.downloader.download_file(url)

    async def download_json(self, url: str) -> typing.Any:
        await asyncio.sleep(self.delay.total_seconds())
        return await self.downloader.download_json(url)
