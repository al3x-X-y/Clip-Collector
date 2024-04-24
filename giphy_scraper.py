import os
import requests
import giphy_client
from giphy_client.rest import ApiException
from API_KEYS import GIPHY_API_KEY


class GiphyScraper:
    def __init__(self, lang="en"):
        self.api_instance = giphy_client.DefaultApi()
        self.api_key = GIPHY_API_KEY  # Use the imported Giphy API key
        self.lang = lang

    def get_gifs_links(self, query):
        try:
            api_response = self.api_instance.gifs_search_get(
                self.api_key, query, lang=self.lang
            )
            return [gif.images.original.url for gif in api_response.data]
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
            return []

    def get_sticker_links(self, query):
        try:
            api_response = self.api_instance.stickers_search_get(
                self.api_key, query, lang=self.lang
            )
            return [sticker.images.original.url for sticker in api_response.data]
        except ApiException as e:
            print("Exception when calling DefaultApi->stickers_search_get: %s\n" % e)
            return []

    def download(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download {filename}")


# Usage
if __name__ == "__main__":
    scraper = GiphyScraper("")

    # Create directories
    if not os.path.exists("gifs"):
        os.makedirs("gifs")
    if not os.path.exists("stickers"):
        os.makedirs("stickers")

    # Download GIFs
    for i, gif_url in enumerate(scraper.get_gifs_links("funny cat")):
        scraper.download(gif_url, f"gifs/gif_{i}.gif")

    # Download Stickers
    for i, sticker_url in enumerate(scraper.get_sticker_links("funny cat")):
        scraper.download(sticker_url, f"stickers/sticker_{i}.gif")
