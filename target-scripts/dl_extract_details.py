from pathlib import Path
from bs4 import BeautifulSoup
import csv


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
        # or if the expected structure is not present
        print(
            f"AttributeError while parsing. Title: {title if 'title' in locals() else 'N/A'}, UPC: {upc if 'upc' in locals() else 'N/A'}, Price: {price if 'price' in locals() else 'N/A'}"
        )
        return None
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        return None


def main():
    """
    Main function to orchestrate the extraction of book details from HTML files.
    """
    # Assuming the script is run from the 'book_scrape' directory root
    book_html_dir = Path("../data/books")
    # If running from 'target-scripts', the path to 'data/books' is '../data/books'
    # If running from workspace root 'book_scrape', it would be 'data/books'
    # Let's adjust for being inside target-scripts

    # To make it more robust, let's try to determine path relative to this script file
    script_dir = Path(__file__).parent
    workspace_root = (
        script_dir.parent
    )  # Assumes target-scripts is one level down from workspace root
    book_html_dir = workspace_root / "data" / "books"

    extracted_data = []

    if not book_html_dir.exists() or not book_html_dir.is_dir():
        print(
            f"Error: Directory '{book_html_dir.resolve()}' not found or is not a directory."
        )
        print("Please ensure the directory exists and contains the book HTML files.")
        return

    print(f"Processing HTML files from: {book_html_dir.resolve()}")

    html_files_found = list(book_html_dir.glob("*.html"))
    if not html_files_found:
        print(f"No HTML files found in {book_html_dir.resolve()}.")
        return

    for html_file in html_files_found:
        print(f"Processing file: {html_file.name}...")
        try:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()

            details = extract_book_details(content)
            if details:
                title, upc, price = details
                print(f"  Title: {title}")
                print(f"  UPC: {upc}")
                print(f"  Price: {price}")
                extracted_data.append(details)
            else:
                print(f"  Could not extract details from {html_file.name}.")
        except Exception as e:
            print(f"  Error processing file {html_file.name}: {e}")
        print("-" * 20)

    if extracted_data:
        print(f"\nSuccessfully extracted details for {len(extracted_data)} books.")
        output_csv_file = workspace_root / "data" / "extracted_book_details.csv"
        try:
            with open(output_csv_file, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Title", "UPC", "Price"])  # Header row
                writer.writerows(extracted_data)
            print(f"Extracted data saved to {output_csv_file.resolve()}")
        except IOError as e:
            print(f"Error saving data to CSV {output_csv_file.resolve()}: {e}")
    else:
        print("\nNo details were extracted from any files.")


if __name__ == "__main__":
    main()
