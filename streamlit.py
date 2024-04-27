import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO
import base64
from giphy_scraper import GiphyScraper
#from flaticon_scraper import FlaticonScraper

# Initialize GiphyScraper
giphy_scraper = GiphyScraper()

# Initialize FlaticonScraper
#flaticon_scraper = FlaticonScraper()

# Set page configuration
st.set_page_config(layout="wide")

# Initialize FlaticonScraper
#flaticon_scraper = FlaticonScraper()

def get_image_download_link(img_url, filename):
    # Get the image data
    response = requests.get(img_url)
    img_data = response.content

    # Encode the image data
    b64 = base64.b64encode(img_data).decode()

    # Create the download link
    href = f'<a href="data:image/gif;base64,{b64}" download="{filename}">Download</a>'

    return href


def display_gifs(gifs, gifs_per_row):
    rows = len(gifs)  # Each gif and its download button will be in a separate row
    for i in range(rows):
        cols = st.columns(
            gifs_per_row * 2
        )  # Double the number of columns to accommodate the download buttons
        for j in range(gifs_per_row):
            index = i * gifs_per_row + j
            if index < len(gifs):  # Check if there is a gif at this index
                cols[j * 2].image(gifs[index], width=200)  # Set width to desired value
                cols[j * 2 + 1].markdown(
                    get_image_download_link(gifs[index], f"gif_{index}.gif"),
                    unsafe_allow_html=True,
                )



# Function to display icons
def display_icons(icons):
    for icon_path in icons:
        with open(icon_path, "rb") as f:
            icon_bytes = f.read()
            st.image(Image.open(BytesIO(icon_bytes)), use_column_width=True)

def main():
    st.title("GIFs and Icons Search")

    # Search box
    search_term = st.text_input("Enter search term:")
    gifs_per_row = st.slider(
        "Number of GIFs per row:", min_value=1, max_value=10, value=5
    )

    if st.button("Search"):
        if search_term:
            st.subheader("GIFs:")
            gifs = giphy_scraper.get_gifs_links(search_term)
            display_gifs(gifs, gifs_per_row)

            st.subheader("Icons:")
            # icons = flaticon_scraper.get_icon_links(search_term)
            # display_icons(icons)
        else:
            st.warning("Please enter a search term.")


if __name__ == "__main__":
    main()
