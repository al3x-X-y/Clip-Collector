import os
import requests
import giphy_client
from giphy_client.rest import ApiException


class GiphyScraper:
    def __init__(self, api_key, query, limit=5, lang="en"):
        self.api_instance = giphy_client.DefaultApi()
        self.api_key = api_key
        self.query = query
        self.limit = limit
        self.lang = lang

    def download_gifs(self):
        try:
            # Search Endpoint
            api_response = self.api_instance.gifs_search_get(
                self.api_key, self.query, limit=self.limit, lang=self.lang
            )

            # Create a directory to save the GIFs
            if not os.path.exists("gifs"):
                os.makedirs("gifs")

            # Loop through each GIF in the response
            for i, gif in enumerate(api_response.data):
                # Get the URL of the GIF
                gif_url = gif.images.original.url
                # Send a GET request to the GIF URL
                gif_response = requests.get(gif_url)
                # Check the status of the request
                if gif_response.status_code == 200:
                    # Open a new file in write mode and save the GIF
                    with open(f"gifs/gif_{i}.gif", "wb") as f:
                        f.write(gif_response.content)
                else:
                    print(f"Failed to download GIF {i}")
        except ApiException as e:
            print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

    def download_stickers(self):
        try:
            # Search Endpoint
            api_response = self.api_instance.stickers_search_get(
                self.api_key, self.query, limit=self.limit, lang=self.lang
            )

            # Create a directory to save the stickers
            if not os.path.exists("stickers"):
                os.makedirs("stickers")

            # Loop through each sticker in the response
            for i, sticker in enumerate(api_response.data):
                # Get the URL of the sticker
                sticker_url = sticker.images.original.url
                # Send a GET request to the sticker URL
                sticker_response = requests.get(sticker_url)
                # Check the status of the request
                if sticker_response.status_code == 200:
                    # Open a new file in write mode and save the sticker
                    with open(f"stickers/sticker_{i}.gif", "wb") as f:
                        f.write(sticker_response.content)
                else:
                    print(f"Failed to download sticker {i}")
        except ApiException as e:
            print("Exception when calling DefaultApi->stickers_search_get: %s\n" % e)


# Usage
scraper = GiphyScraper("XbIwaoR4IQwNNcGMvgTdYGtB8kMq03EA", "funny cat")
scraper.download_gifs()
scraper.download_stickers()
