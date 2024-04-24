import argparse
import os
import sys
import requests
from uuid import uuid4
from API_KEYS import TENOR_API_KEY

# Define constants
RESOLUTIONS = [16, 24, 32, 64, 128, 256, 512]

class TenorScraper:
    def __init__(self, api_key: str):
        self.api_key = TENOR_API_KEY
        self.session = requests.Session()

    def parse_arguments(self, args: list[str]) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Download Tenor GIFs")
        parser.add_argument("search", type=str, help="Search query for Tenor GIFs")
        parser.add_argument(
            "-o", "--output", type=str, default=os.getcwd(), help="Output directory"
        )
        return parser.parse_args(args)

    def get_image_url(self, keyword: str) -> list[str]:
        url = f"https://api.tenor.com/v1/search?q={keyword}&key={self.api_key}"
        try:
            response = self.session.get(url)
            results = response.json()
            urls = [
                result["media"][0]["mediumgif"]["url"]
                for result in results.get("results", [])
            ]
            return urls
        except (requests.ConnectionError, requests.Timeout) as err:
            print(f"Error fetching Tenor GIFs: {err}")
            return []

    def download(self, url: str, output_dir: str):
        output_file = os.path.join(output_dir, f"{uuid4()}.gif")
        try:
            response = self.session.get(url)
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {url}")
        except (requests.ConnectionError, requests.Timeout) as err:
            print(f"Error downloading GIF: {err}")

    def main(self):
        args = self.parse_arguments(sys.argv[1:])
        search_query = args.search
        output_dir = args.output

        urls = self.get_image_url(search_query)
        if not urls:
            print("No GIFs found.")
            return

        os.makedirs(output_dir, exist_ok=True)
        for url in urls:
            self.download(url, output_dir)


if __name__ == "__main__":
    downloader = TenorScraper(TENOR_API_KEY)
    downloader.main
