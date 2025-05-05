import requests
from pathlib import Path

# make page folder, and save the html files
page_folder = Path("./data/pages")
page_folder.mkdir(parents=True, exist_ok=True)

for i in range(1,51):
    url = f"http://books.toscrape.com/catalogue/page-{i}.html"

    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        filepath = page_folder / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Page {i} saved successfully.")
    else:
        print(f"Failed to retrieve page {i}. Status code: {response.status_code}")


