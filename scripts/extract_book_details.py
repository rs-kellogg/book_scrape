\
import csv
from pathlib import Path
from bs4 import BeautifulSoup
import re

def parse_book_html(html_content):
    """Parses HTML content of a book page to extract title, price, and UPC."""
    soup = BeautifulSoup(html_content, 'html.parser')

    title = None
    price = None
    upc = None

    # Extract Title
    # Example: <div class="col-sm-6 product_main"> <h1>A Light in the Attic</h1>
    product_main_div = soup.find('div', class_='product_main')
    if product_main_div:
        title_tag = product_main_div.find('h1')
        if title_tag and title_tag.string:
            title = title_tag.string.strip()

    # Extract Price
    # Example: <p class="price_color">Â£51.77</p>
    price_tag = soup.find('p', class_='price_color')
    if price_tag and price_tag.string:
        # Use regex to extract only the numerical part of the price, handling potential currency symbols
        price_match = re.search(r'([£$€]?)([\d\.]+)', price_tag.string.strip())
        if price_match:
            price = price_match.group(2) # Get the numeric part

    # Extract UPC
    # Example: <table class="table table-striped"> ... <tr> <th>UPC</th><td>a897fe39b1053632</td> </tr> ... </table>
    product_info_table = soup.find('table', class_='table-striped')
    if product_info_table:
        for row in product_info_table.find_all('tr'):
            header = row.find('th')
            if header and header.string and header.string.strip() == 'UPC':
                value_cell = row.find('td')
                if value_cell and value_cell.string:
                    upc = value_cell.string.strip()
                break
    
    return title, price, upc

def main():
    """
    Iterates through downloaded HTML book files, extracts details (title, price, UPC),
    and saves them to a CSV file.
    """
    # Determine paths relative to the script file
    script_location = Path(__file__).resolve()
    base_dir = script_location.parent.parent # Moves up two levels (scripts -> book_scrape)
    
    books_dir = base_dir / "data" / "books"
    output_csv_path = base_dir / "data" / "extracted_book_details.csv"
    
    extracted_data = []

    if not books_dir.is_dir():
        print(f"Error: Directory not found: {books_dir}")
        print("Please ensure the script is in the 'scripts' directory and 'data/books' exists.")
        return

    print(f"Scanning for HTML files in: {books_dir}")
    html_files = list(books_dir.glob("*.html"))

    if not html_files:
        print(f"No HTML files found in {books_dir}.")
        return

    print(f"Found {len(html_files)} HTML files to process.")

    for html_file in html_files:
        print(f"Processing {html_file.name}...")
        try:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            title, price, upc = parse_book_html(content)
            
            if title or price or upc: # Add to list if at least one item was found
                extracted_data.append({
                    "filename": html_file.name,
                    "title": title,
                    "price": price,
                    "upc": upc,
                })
                print(f"  Title: {title if title else 'Not found'}")
                print(f"  Price: {price if price else 'Not found'}")
                print(f"  UPC: {upc if upc else 'Not found'}")
            else:
                print(f"  Could not extract any details for {html_file.name}.")
            
        except Exception as e:
            print(f"  Error processing file {html_file.name}: {e}")
        print("-" * 20)

    if extracted_data:
        print(f"\\nWriting extracted data to {output_csv_path}...")
        try:
            with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["filename", "title", "price", "upc"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(extracted_data)
            print(f"Successfully saved data for {len(extracted_data)} books to {output_csv_path}")
        except IOError as e:
            print(f"Error writing CSV file: {e}")
    else:
        print("\\nNo data was extracted to save.")

if __name__ == "__main__":
    main()
