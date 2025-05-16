import requests
from pathlib import Path
import csv

book_list = []
with open("data/books_list.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:  # Ensure the row is not empty
            book_list.append(row[1])
print(book_list)


def download_book_page(url, book_folder, book_index):
    """Downloads a single book page and saves it as an HTML file."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        # Ensure there are enough parts in the URL to avoid IndexError
        url_parts = url.split("/")
        if len(url_parts) >= 2:
            filename = url_parts[-2] + ".html"
        else:
            # Fallback filename if URL structure is unexpected
            filename = f"book_{book_index + 1}.html"
        filepath = book_folder / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Book {book_index + 1} saved successfully as {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve book {book_index + 1} from {url}. Error: {e}")


def main():
    """Downloads book pages from a list of URLs and saves them as HTML files.

    The function iterates through a predefined `book_list` of URLs.
    For each URL, it attempts to download the page content.
    The content is saved as an HTML file in the './data/books' directory.
    The directory is created if it doesn't already exist.
    Filenames are derived from the URL.

    Messages are printed to the console indicating success or failure.
    """
    book_folder = Path("./data/books")
    book_folder.mkdir(parents=True, exist_ok=True)

    for i, url in enumerate(book_list):
        download_book_page(url, book_folder, i)


if __name__ == "__main__":
    main()
