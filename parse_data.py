# parse_data.py
from bs4 import BeautifulSoup

def parse_data(driver):
    """Parse the HTML page and extract relevant data."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tables = soup.find_all("table")

    if len(tables) > 1:
        table = tables[1]  # Access the second table
        headers = [header.text.strip() for header in table.find_all("th")]
        rows = []
        for row in table.find_all("tr"):
            cells = [cell.text.strip() for cell in row.find_all("td")]
            if cells:
                rows.append(cells)
        return headers, rows
    else:
        return [], []
