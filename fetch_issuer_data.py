import datetime
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def fetch_issuer_data(driver, issuer_code, end_date, csv_writer, last_date=None):
    """Fetch data for a specific issuer code starting from the last available date."""
    url = f"https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}"
    driver.get(url)

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 20)

    # If there's no last date, start from 10 years ago
    if last_date is None:
        start_date = end_date - datetime.timedelta(days=10 * 365)
    else:
        start_date = last_date + datetime.timedelta(days=1)  # Fetch data from the next day after the last date

    # Loop through years from start_date to the current date
    for i in range(10):
        year_end_date = start_date + datetime.timedelta(days=i * 365)
        year_start_date = year_end_date - datetime.timedelta(days=365)
        date_str_from = year_start_date.strftime("%d.%m.%Y")
        date_str_to = year_end_date.strftime("%d.%m.%Y")

        # Wait for the date fields and fill them
        try:
            from_date_field = wait.until(EC.visibility_of_element_located((By.ID, "FromDate")))
            to_date_field = wait.until(EC.visibility_of_element_located((By.ID, "ToDate")))
            from_date_field.clear()
            from_date_field.send_keys(date_str_from)
            to_date_field.clear()
            to_date_field.send_keys(date_str_to)

            # Click the submit button
            submit_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-primary-sm")))
            submit_button.click()

            # Wait for the table rows to load, if they exist
            try:
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
            except TimeoutException:
                # If rows are not found within the timeout, assume no data is available
                print(f"No data available for {issuer_code} ({date_str_from} to {date_str_to}). Skipping...")
                continue  # Move to the next date range or issuer

            # Parse the page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tables = soup.find_all("table")

            if len(tables) > 1:
                table = tables[1]  # Access the second table
                rows = table.find_all("tr")
                print(f"Number of rows found for {issuer_code}: {len(rows)}")

                for row in rows:
                    cells = [cell.text.strip() for cell in row.find_all("td")]
                    if cells:
                        row_data = [issuer_code, date_str_from, date_str_to] + cells
                        csv_writer.writerow(row_data)  # Write directly to CSV
            else:
                print(f"No data table found for {issuer_code} ({date_str_from} to {date_str_to})")

        except TimeoutException:
            print(f"Timeout while processing {issuer_code} ({date_str_from} to {date_str_to}). Skipping...")
            continue
        except Exception as e:
            print(f"Error occurred for {issuer_code} ({date_str_from} to {date_str_to}): {e}")
            continue
