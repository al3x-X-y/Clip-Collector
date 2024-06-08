import streamlit as st
import urllib.parse
import requests
from PIL import Image
from io import BytesIO
import base64
import asyncio
from giphy_scraper import GiphyScraper
from pexels_scraper import PexelsScraper
from flaticon_scraper import FlaticonScraper

# Initialize GiphyScraper
giphy_scraper = GiphyScraper()

# Initialize FlaticonScraper
flaticon_scraper = FlaticonScraper("default query")

# Initialize PexelsScraper
pelex_scraper = PexelsScraper()


# Set page configuration
st.set_page_config(layout="wide")

class GifDisplay:
    def __init__(self, gifs_dict):
        self.gifs_dict = gifs_dict

    def get_image_download_link(self, img_url, filename):
        # Get the image data
        response = requests.get(img_url)
        img_data = response.content

        # Encode the image data
        b64 = base64.b64encode(img_data).decode()

        # Create the download link
        href = (
            f'<a href="data:image/gif;base64,{b64}" download="{filename}">Download</a>'
        )

        return href

    def display_gifs(self, gifs_per_row):
        for gif_name, gifs in self.gifs_dict.items():
            st.subheader(gif_name)
            rows = min(10, len(gifs))  # Limit to first 10 items
            for i in range(rows):
                cols = st.columns(
                    gifs_per_row * 2
                )  # Double the number of columns to accommodate the download buttons
                for j in range(gifs_per_row):
                    index = i * gifs_per_row + j
                    if index < len(gifs):  # Check if there is a gif at this index
                        cols[j * 2].image(
                            gifs[index], width=200
                        )  # Set width to desired value
                        cols[j * 2 + 1].markdown(
                            self.get_image_download_link(
                                gifs[index], f"gif_{index}.gif"
                            ),
                            unsafe_allow_html=True,
                        )

    def display_videos(self):
        for video_name, videos in self.gifs_dict.items():
            if "video" in video_name.lower():
                st.subheader(video_name)
                for video_url in videos[:10]:  # Limit to first 10 videos
                    st.video(video_url)  # Display the video

    # Function to display icons
    def display_icons(icons):
        for icon_path in icons:
            with open(icon_path, "rb") as f:
                icon_bytes = f.read()
                st.image(Image.open(BytesIO(icon_bytes)), use_column_width=True)

def main():
    # Search box
    search_term = st.text_input("Enter search term:")
    gifs_per_row = st.slider(
        "Number of GIFs per row:", min_value=1, max_value=10, value=5
    )

    if st.button("Search"):
        if search_term:
            # Run the coroutines and get the results
            gifs = asyncio.run(giphy_scraper.get_gifs_links(search_term))
            stickers = asyncio.run(giphy_scraper.get_sticker_links(search_term))
            videos = asyncio.run(
                pelex_scraper.get_media_links(
                    search_term, "videos", 10
                )  # Increase to 10
            )
            pictures = asyncio.run(
                pelex_scraper.get_media_links(
                    search_term, "photos", 10
                )  # Increase to 10
            )
            # Update the query of the FlaticonScraper instance
            flaticon_scraper.query = urllib.parse.quote(search_term)
            # Get the image links
            flaticon = asyncio.run(flaticon_scraper.get_image_links())

            gifs_dict = {
                "Flaticon": flaticon,  # Add the "Flaticon" key to the dictionary
                "GIFs": gifs,
                "Stickers": stickers,
                "Pictures": pictures,
                "Videos": videos,
            }

            gif_display = GifDisplay(gifs_dict)
            gif_display.display_gifs(gifs_per_row)
            gif_display.display_videos()  # Call without arguments

        else:
            st.warning("Please enter a search term.")


# Run the main function
if __name__ == "__main__":
    main()
