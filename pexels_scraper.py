import requests
import asyncio
from API_KEYS import PEXELS_API_KEY


class PexelsScraper:
    def __init__(self):
        self.API_KEY = PEXELS_API_KEY
        self.headers = {"Authorization": self.API_KEY}

    async def get_media_links(self, query, media_type, limit):
        url = f"https://api.pexels.com/v1/search?query={query}&per_page={limit}&page=1"
        if media_type == "videos":
            url = f"https://api.pexels.com/videos/search?query={query}&per_page={limit}&page=1"

        response = requests.get(url, headers=self.headers)
        response_json = response.json()

        if media_type == "videos":
            if "videos" in response_json:
                return [
                    video["video_files"][0]["link"] for video in response_json["videos"]
                ]
            else:
                return []
        else:
            if "photos" in response_json:
                return [photo["src"]["original"] for photo in response_json["photos"]]
            else:
                return []

    def download_media(self, links, media_type):
        for i, link in enumerate(links):
            file_name = f"{media_type}_{i}.{'mp4' if media_type == 'videos' else 'jpg'}"
            print(f"Downloading {media_type[:-1]}:", file_name)

            r = requests.get(link, stream=True)

            with open(file_name, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"{file_name} downloaded!")


if __name__ == "__main__":
    pexels_downloader = PexelsScraper()

    search_query = "cat"
    video_limit = 5
    photo_limit = 5

    video_links = asyncio.run(
        pexels_downloader.get_media_links(search_query, "videos", video_limit)
    )
    pexels_downloader.download_media(video_links, "videos")

    photo_urls = asyncio.run(
        pexels_downloader.get_media_links(search_query, "photos", photo_limit)
    )
    pexels_downloader.download_media(photo_urls, "photos")
