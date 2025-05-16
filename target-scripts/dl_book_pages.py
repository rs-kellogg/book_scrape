import requests
from pathlib import Path
import csv
import sys
from bs4 import BeautifulSoup


def extract_book_details(html_content: str) -> tuple[str, str, str] | None:
    """
    Extracts the title, UPC, and price from the HTML content of a book page.

    Args:
        html_content: The HTML content of the book page.

    Returns:
        A tuple containing the title, UPC, and price (all as strings).
        Returns None if any of the details cannot be found.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    try:
        # Extract title
        title_tag = soup.find("div", class_="product_main").find("h1")
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract UPC
        upc_header = soup.find("th", string="UPC")
        upc = (
            upc_header.find_next_sibling("td").text.strip()
            if upc_header and upc_header.find_next_sibling("td")
            else "N/A"
        )

        # Extract price
        price_tag = soup.find("p", class_="price_color")
        price = price_tag.text.strip() if price_tag else "N/A"

        return title, upc, price
    except AttributeError:
        # Handle cases where elements might be missing leading to None.find()
        return None


def download_book(url, book_folder, book_index):
    """Downloads a single book from the given URL and saves it to the specified folder."""
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-2] + ".html"
        filepath = book_folder / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Book {book_index + 1} saved successfully.")
    else:
        print(
            f"Failed to retrieve book {book_index + 1}. Status code: {response.status_code}"
        )


def main():
    """Main function to orchestrate the book downloading process."""
    book_list = []
    with open("data/books_list.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Ensure the row is not empty
                book_list.append(row[1])

    print(book_list)
    for i, url in enumerate(book_list):
        download_book(url, book_folder, i)

    # Extract book details from the downloaded HTML file
    for i, url in enumerate(book_list):
        filename = url.split("/")[-2] + ".html"
        filepath = book_folder / filename
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()
            book_details = extract_book_details(html_content)
            if book_details:
                title, upc, price = book_details
                print(f"Book {i + 1}: Title: {title}, UPC: {upc}, Price: {price}")
            else:
                print(f"Failed to extract details for book {i + 1}.")
            


if __name__ == "__main__":
    if len(sys.argv) > 1:
        book_folder = Path(sys.argv[1])
    else:
        book_folder = Path("./data/books")
    book_folder.mkdir(parents=True, exist_ok=True)
    main()
