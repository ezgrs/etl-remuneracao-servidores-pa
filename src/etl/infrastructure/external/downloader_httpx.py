from etl.application.ports.downloader import Downloader


import httpx


class HttpxDownloader(Downloader):
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def download_html(self, url: str) -> str:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.text

    async def download_file(self, url: str) -> bytes:
        response = await self._client.get(url)
        response.raise_for_status()
        return response.content
