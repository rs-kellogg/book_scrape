import requests
from pathlib import Path

book_list = ["http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
            "http://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html",
            "http://books.toscrape.com/catalogue/sophies-world_966/index.html", 
            "http://books.toscrape.com/catalogue/shoe-dog-a-memoir-by-the-creator-of-nike_831/index.html",
            "http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
            ]

book_folder = Path("./data/books")
book_folder.mkdir(parents=True, exist_ok=True)

for i, url in enumerate(book_list):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-2] + ".html"
        filepath = book_folder / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Book {i+1} saved successfully.")
    else:
        print(f"Failed to retrieve book {i+1}. Status code: {response.status_code}")


