import streamlit as st
from flaticon_scraper import FlaticonScraper
from giphy_scraper import GiphyScraper
from pexels_scraper import PexelsScraper
from tenor_scraper import TenorScraper

# Initialize scrapers
flaticon_scraper = FlaticonScraper()
giphy_scraper = GiphyScraper()
# pexels_scraper = PexelsScraper()
# tenor_scraper = TenorScraper()


def main():
    st.title("Media Search")

    # Search form
    with st.form(key="searchform"):
        search_term = st.text_input("Search")
        submit_search = st.form_submit_button(label="Search")

    if submit_search:
        # Fetch and display gifs from Giphy
        gifs = giphy_scraper.search(search_term, page=0)
        for gif in gifs:
            if st.button("Download GIF", key=gif["id"]):
                giphy_scraper.download(gif["id"])

        # Fetch and display videos from Pexels
        # videos = pexels_scraper.search_videos(search_term, page=0)
        # for video in videos:
        #     if st.button('Download Video', key=video['id']):
        #         pexels_scraper.download_video(video['id'])

        # # Fetch and display photos from Pexels
        # photos = pexels_scraper.search_photos(search_term, page=0)
        # for photo in photos:
        #     if st.button('Download Photo', key=photo['id']):
        #         pexels_scraper.download_photo(photo['id'])

        # Fetch and display icons from Flaticon
        icons = flaticon_scraper.search(search_term, page=0)
        for icon in icons:
            if st.button("Download Icon", key=icon["id"]):
                flaticon_scraper.download(icon["id"])


if __name__ == "__main__":
    main()
