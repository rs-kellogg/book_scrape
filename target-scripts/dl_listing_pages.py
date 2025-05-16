import requests
from pathlib import Path
import sys


def download_page(url: str, page_folder: Path, i: int) -> None:
    """
    Downloads the content of a web page and saves it to a specified folder.
    Args:
        url (str): The URL of the web page to download.
        page_folder (Path): The directory where the downloaded page will be saved.
        i (int): The index or identifier for the page, used for logging purposes.
    Returns:
        None
    Side Effects:
        Saves the downloaded HTML content to a file in the specified folder.
        Prints a message indicating success or failure of the download.
    """
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        filepath = page_folder / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Page {i} saved successfully.")
    else:
        print(f"Failed to retrieve page {i}. Status code: {response.status_code}")


def main(num_pages):
    """
    Downloads and saves HTML pages from 'books.toscrape.com' for a given number of pages.
    Args:
        num_pages (int): The number of pages to download and save.

    Creates:
        A directory './data/pages' (if it does not exist) and saves each downloaded HTML page
        as a file within this directory.
    """
    # make page folder, and save the html files
    page_folder = Path("./data/pages")
    page_folder.mkdir(parents=True, exist_ok=True)
    for i in range(1, num_pages + 1):
        url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        download_page(url, page_folder, i)


if __name__ == "__main__":
    num_pages = 50
    if len(sys.argv) > 1:
        try:
            num_pages = int(sys.argv[1])
        except ValueError:
            print("Invalid number of pages. Using default (50).")
    main(num_pages)
