# Clip Collector

Clip Collector is a web application that allows users to search and download images and GIFs from Giphy, Pexels, Tenor, and Flaticon using Streamlit. This project uses various APIs and a custom scraper to gather and display media content. 
<br>


This tool will be useful for video editors who visits multiple websites to search and download media files. With Clip Collector, you only need to search once to download all the media you need with a single click.
## Features

- **Search and Download**: Search and download images and GIFs from Giphy, Pexels, Tenor, and Flaticon.
- **Streamlit Interface**: User-friendly web interface built with Streamlit.
- **Custom Scraper**: Custom scraping functionality for Flaticon.
- **Random User-Agent**: Uses a random user-agent for requests to avoid being blocked.

## Libraries Used

The project makes use of the following libraries:

- `streamlit`
- `urllib.parse`
- `requests`
- `PIL` (Python Imaging Library)
- `io.BytesIO`
- `base64`
- `asyncio`
- `giphy_client`
- `lxml.html`
- `argparse`
- `uuid`

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/easy-downloader.git
    cd easy-downloader
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up API keys for Giphy, Pexels, and Tenor. You can obtain these keys from their respective developer portals and set them as environment variables:

    ```sh
    export GIPHY_API_KEY='your_giphy_api_key'
    export PEXELS_API_KEY='your_pexels_api_key'
    export TENOR_API_KEY='your_tenor_api_key'
    ```

## Usage

Run the Streamlit app:

```sh
streamlit run app.py
```


## Contributing
Contributions are welcome! Please follow these steps to contribute:

  * Fork the repository:
```sh
git checkout -b feature-branch
```
   Make your changes.
  * Commit your changes :
```sh
git commit -m 'Add new feature'
```
* Push to the branch :
```sh
git push origin feature-branch
```
  Open a pull request.


<br>



### License
This project is licensed under the MIT License.

### Acknowledgements
[Giphy API](https://developers.giphy.com/) 

[Pexels API](https://www.pexels.com/api/documentation/)

[Tenor API](https://tenor.com/gifapi/documentation)

[Flaticon](https://www.flaticon.com/)
