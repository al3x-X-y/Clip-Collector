from flaticon_scraper import FlaticonScraper
from giphy_scraper import GiphyScraper
from pexels_scraper import PexelsScraper
from tenor_scraper import TenorScraper
from API_KEYS import (
    FLATICON_API_KEY,
    GIPHY_API_KEY,
    PEXELS_API_KEY,
    TENOR_API_KEY,
)  # Import the API keys

# Initialize the scraper objects
FlaticonScraper = FlaticonScraper()
GiphyScraper = GiphyScraper(GIPHY_API_KEY)
PexelsScraper = PexelsScraper(PEXELS_API_KEY)
TenorScraper = TenorScraper(TENOR_API_KEY)

def main():
    # Define the search query
    query = "funny cat"

    # Get and download icons from Flaticon
    for i, url in enumerate(FlaticonScraper.get_image_links(query)):
        FlaticonScraper.download(url, f"flaticon/icon_{i}.png")

    # Get and download GIFs from Giphy
    for i, url in enumerate(GiphyScraper.get_gifs_links(query)):
        GiphyScraper.download(url, f"giphy/gif_{i}.gif")

    # Get and download images from Pexels# Get and download images from Pexels
    for i, url in enumerate(PexelsScraper.get_photos_links(query)):
        PexelsScraper.download(url, f"pexels/photo_{i}.jpg")

    # Get and download GIFs from Tenor
    for i, url in enumerate(TenorScraper.get_gifs_links(query)):
        TenorScraper.download(url, f"tenor/gif_{i}.gif")


if __name__ == "__main__":
    main()
