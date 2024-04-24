#!/usr/bin/python3
import argparse
import os
import random
import sys

import requests
from lxml import html

import USER_AGENTS

RESOLUTIONS = [16, 24, 32, 64, 128, 256, 512]
DOWNLOAD_URL = "https://cdn-icons-png.flaticon.com/{res}/{part}/{img}.png"


class FlaticonScraper:
    def __inti__(self):
        pass

    def download(self, image_url, output_file):
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        response = requests.get(image_url, allow_redirects=True)
        open(output_file, "wb").write(response.content)

    def get_image_url(self, page_url, image_resolution):
        image_type = self.define_type(page_url)
        result = []
        if image_type == 0:
            page = requests.get(
                page_url, headers={"User-Agent": random.choice(USER_AGENTS.USER_AGENTS)}
            )
            img = html.fromstring(page.text).xpath(".//img[@class='img-small']/@src")
            img = img.rsplit("/", 3)
            if image_resolution == 0:
                for i in RESOLUTIONS:
                    img[1] = str(i)
                    result.append("/".join(img))
            else:
                img[1] = str(image_resolution)
                result.append("/".join(img))
        elif image_type == 1:
            img = page_url.rsplit("_", 1)[1]
            part = img[: len(img) - 3]
            if image_resolution == 0:
                for i in RESOLUTIONS:
                    result.append(DOWNLOAD_URL.format(res=i, part=part, img=img))
            else:
                result.append(
                    DOWNLOAD_URL.format(res=image_resolution, part=part, img=img)
                )
        elif image_type == 2:
            page = requests.get(
                page_url, headers={"User-Agent": random.choice(USER_AGENTS.USER_AGENTS)}
            )
            imgs = html.fromstring(page.text).xpath(
                ".//a[contains(@class, 'view')]/img/@data-src"
            )
            for url in imgs:
                url = url.rsplit("/", 3)
                url[1] = str(image_resolution)
                result.append("/".join(url))
        elif image_type == 3:
            page = requests.get(
                page_url,
                headers={"User-Agent": random.choice(USER_AGENTS.USER_AGENTS)},
                timeout=10,
            )  # Increase timeout to 10 seconds

            imgs = html.fromstring(page.text).xpath(
                ".//li[contains(@class, 'icon--item')][@data-png]/@data-png"
            )
            for url in imgs:
                url = url.rsplit("/", 3)
                url[1] = str(image_resolution)
                result.append("/".join(url))
        return result

    def define_type(self, page_url):
        if page_url.startswith("https://www.flaticon.com/search"):
            return 3
        elif page_url.startswith("https://www.flaticon.com/packs"):
            return 2
        elif page_url.startswith("https://www.flaticon.com/free-icon"):
            return 1
        elif page_url.startswith("https://www.flaticon.com/premium-icon"):
            return 0


scraper = FlaticonScraper()
scraper.download(image_url, output_file)
