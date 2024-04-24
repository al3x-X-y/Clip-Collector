# Specify the search query
import os
from requests import get
import requests
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import random
from USER_AGENTS import USER_AGENTS


# Specify the API key for Pexels
PEXELS_API_KEY = "api"


# Specify the search query
search_query = "cat"

# Specify the base URL for Pexels videos
pexels_base_url = f"https://api.pexels.com/videos/search?query={search_query}&per_page="

# Specify the base URL for Pexels photos
pexels_photos_base_url = (
    f"https://api.pexels.com/v1/search?query={search_query}&per_page="
)


class PexelsDownloader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": api_key,
            "User-Agent": USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)],
        }

    def get_video_links(self, limit):
        response = requests.get(
            pexels_base_url + str(limit), headers=self.headers, verify=False
        )
        if response.status_code == 200:
            data = response.json()
            return [video["video_files"][0]["link"] for video in data["videos"]]
        else:
            print("Error: Failed to fetch video links")
            return []

    def download_video_series(self, video_links, limit):
        for i, link in enumerate(video_links, 1):
            # Obtain filename by splitting URL and getting the last string
            file_name = f"video_{i}.mp4"
            print("Downloading video:", file_name)

            # Create response object
            r = requests.get(link, stream=True, verify=False)

            # Download started
            with open(file_name, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"{file_name} downloaded!")

            # Editing the video
            song_choice = random.choice(range(1, 6))  # Assuming 5 audio files available
            clip = VideoFileClip(file_name)
            clip_duration = clip.duration
            audioclip = AudioFileClip(f"songs/audio{song_choice}.mp3").set_duration(
                clip_duration
            )
            new_audioclip = CompositeAudioClip([audioclip])
            final_clip = clip.set_audio(new_audioclip)
            final_clip.write_videofile(f"videos/edited_video_{i}.mp4", fps=60)
            print(f"{file_name} has been edited!\n")

    def get_photo_urls(self, limit):
        response = requests.get(
            pexels_photos_base_url + str(limit), headers=self.headers, verify=False
        )
        if response.status_code == 200:
            data = response.json()
            return [photo["src"]["original"] for photo in data["photos"]]
        else:
            print("Error: Failed to fetch photo URLs")
            return []

    def download_photos(self, photo_urls, limit):
        for i, url in enumerate(photo_urls, 1):
            # Obtain filename by splitting URL and getting the last string
            file_name = f"photo_{i}.jpg"
            print("Downloading photo:", file_name)

            # Create response object
            r = requests.get(url, stream=True, verify=False)

            # Download started
            with open(file_name, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

            print(f"{file_name} downloaded!")


if __name__ == "__main__":
    pexels_downloader = PexelsDownloader(PEXELS_API_KEY)

    # Getting all video links from Pexels API
    video_limit = 5  # Limit for videos to download
    video_links = pexels_downloader.get_video_links(video_limit)

    # Downloading and editing all videos
    pexels_downloader.download_video_series(video_links, video_limit)

    # Getting all photo URLs from Pexels API
    photo_limit = 5  # Limit for photos to download
    photo_urls = pexels_downloader.get_photo_urls(photo_limit)

    # Downloading all photos
    pexels_downloader.download_photos(photo_urls, photo_limit)
