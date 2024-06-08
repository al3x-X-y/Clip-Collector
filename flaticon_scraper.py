import os
import random
import requests
import urllib.parse
from lxml import html
import asyncio
import USER_AGENTS

RESOLUTIONS = [16, 24, 32, 64, 128, 256, 512]
DOWNLOAD_URL = "https://cdn-icons-png.flaticon.com/{res}/{part}/{img}.png"


class FlaticonScraper:
    BASE_URL = "https://www.flaticon.com/search"

    def __init__(self, query):
        self.query = urllib.parse.quote(query)  # URL-encode the query string

    async def download(self, image_url, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        response = requests.get(image_url, allow_redirects=True)
        with open(filename, "wb") as f:
            f.write(response.content)

    async def get_image_links(self):
        imgs = []
        page_url = f"{self.BASE_URL}?word={self.query}"  # Construct the URL
        image_type = await self.define_type(page_url)
        result = []
        page = requests.get(
            page_url, headers={"User-Agent": random.choice(USER_AGENTS.USER_AGENTS)}
        )
        if image_type == 0:
            imgs = html.fromstring(page.text).xpath(".//img[@class='img-small']/@src")
        elif image_type == 1:
            imgs = [page_url.rsplit("_", 1)[1]]
        elif image_type == 2:
            imgs = html.fromstring(page.text).xpath(
                ".//a[contains(@class, 'view')]/img/@data-src"
            )
        elif image_type == 3:
            imgs = html.fromstring(page.text).xpath(
                ".//li[contains(@class, 'icon--item')][@data-png]/@data-png"
            )
        print (imgs)
        for url in imgs:
            result.append(url)
        return imgs

    async def define_type(self, page_url):
        if page_url.startswith("https://www.flaticon.com/search"):
            return 3
        elif page_url.startswith("https://www.flaticon.com/packs"):
            return 2
        elif page_url.startswith("https://www.flaticon.com/free-icon"):
            return 1
        else:
            return 0




if __name__ == "__main__":
    scraper = FlaticonScraper("cat")
    image_links = asyncio.run(scraper.get_image_links())
    for i, image_link in enumerate(image_links):
        scraper.download(image_link, f"flaticon/icon_{i}.png")
