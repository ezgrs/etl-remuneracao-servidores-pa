import hashlib
import json
import typing

import aiopath

from etl.application.ports.downloader import Downloader


class CachedDownloader(Downloader):
    downloader: Downloader
    path: aiopath.AsyncPath

    def __init__(
        self, downloader: Downloader, *, path: aiopath.AsyncPath
    ) -> None:
        self.downloader = downloader
        self.path = path

    async def _ensure_dir(self) -> None:
        await self.path.mkdir(parents=True, exist_ok=True)

    def _key(self, url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    async def download_html(self, url: str) -> str:
        await self._ensure_dir()

        file_path = self.path / f"html_{self._key(url)}"

        if await file_path.exists():
            return await file_path.read_text(encoding="utf-8")

        content = await self.downloader.download_html(url)
        await file_path.write_text(content, encoding="utf-8")
        return content

    async def download_file(self, url: str) -> bytes:
        await self._ensure_dir()

        file_path = self.path / f"file_{self._key(url)}"

        if await file_path.exists():
            return await file_path.read_bytes()

        data = await self.downloader.download_file(url)
        await file_path.write_bytes(data)
        return data

    async def download_json(self, url: str) -> typing.Any:
        await self._ensure_dir()

        file_path = self.path / f"json_{self._key(url)}"

        if await file_path.exists():
            data = await file_path.read_text(encoding="utf-8")
            return json.loads(data)

        data = await self.downloader.download_json(url)
        await file_path.write_text(json.dumps(data), encoding="utf-8")
        return data
