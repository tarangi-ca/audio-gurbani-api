import re
from typing import Annotated

import httpx
from bs4 import BeautifulSoup, NavigableString, Tag
from fastapi import Depends
from hukamnama.exceptions import (
    InvalidFormatException,
    MissingElementException,
    PageFetchException,
)
from hukamnama.models import HukamnamaRecord
from hukamnama.repository import HukamnamaRepository
from hukamnama.schemas import MehlMapping


class HukamnamaScraper:
    HUKAMNAMA_URL = "https://hs.sgpc.net/index.php"

    def __init__(self, repository: Annotated[HukamnamaRepository, Depends()]):
        self.repository = repository

    async def fetch(self) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response: httpx.Response = await client.get(
                    self.HUKAMNAMA_URL, timeout=30.0
                )
                response.raise_for_status()
                return response.text
        except (httpx.RequestError, httpx.HTTPStatusError):
            raise PageFetchException(
                f"Failed to fetch the page at {
                self.HUKAMNAMA_URL}"
            )

    def parse(self, html: str):
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

        reference = soup.find("strong", string=re.compile(r"English Translation", re.I))

        if not reference:
            raise MissingElementException("Reference point not found.")

        container: Tag | NavigableString | None = reference.find_next(
            "div", class_="b3 mt-4 mb-3"
        )

        if not container:
            raise MissingElementException("Container not found.")

        melody, writer = self.parse_heading(container)
        return {
            "melody": melody,
            "writer": writer,
            "text": self.parse_text(container),
            "page": self.parse_page(soup),
        }

    def parse_heading(
        self, container: Tag | NavigableString
    ) -> tuple[str, MehlMapping]:
        heading: Tag | NavigableString | None = container.find_next(
            "div", class_="text-center"
        )

        if not heading:
            raise MissingElementException("Heading not found.")

        components: list[str] = (
            heading.get_text().replace(":", "").strip().replace("MEHL", "").split(",")
        )

        if len(components) != 2:
            raise InvalidFormatException("Invalid heading format.")

        return (
            components[0].strip().title(),
            MehlMapping[components[1].strip().upper()],
        )

    def parse_text(self, container: Tag | NavigableString) -> str:
        text: Tag | NavigableString | None = container.find_next("div", class_="")

        if not text:
            raise MissingElementException("Text not found.")

        return text.get_text().strip()

    def parse_page(self, soup: BeautifulSoup) -> int:
        page: Tag | NavigableString | None = soup.find(
            "c1", string=re.compile(r"Ang|Page", re.I)
        )

        if not page:
            raise MissingElementException("Page not found.")

        component: re.Match | None = re.search(r"\d+", page.get_text())

        if not component:
            raise InvalidFormatException("Invalid page format.")

        return int(component.group())

    async def run(self) -> HukamnamaRecord | None:
        html = await self.fetch()
        if not html:
            return
        return await self.repository.create(**self.parse(html))
