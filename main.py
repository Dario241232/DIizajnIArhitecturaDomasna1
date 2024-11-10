import datetime
import csv
from final.fetch_issuer_codes import fetch_issuer_codes
from final.fetch_issuer_data import fetch_issuer_data
from process_data import get_last_date_from_csv
from final.driver_setup import setup_driver  # Ensure this import is correct

# Set up WebDriver
driver = setup_driver()  # This initializes the driver correctly

# Define current date
end_date = datetime.datetime.today()

# Open the CSV file in write mode
csv_file = "mse_data.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file)

    # Write headers
    headers = ["Issuer Code", "From Date", "To Date", "Date", "LastTransaction", "Max", "Min", "Average", "%Prom", "Quantity", "Traffic BEST in denars", "TotalTraffic in denars"]  # Add actual header names
    csv_writer.writerow(headers)

    # Fetch issuer codes
    issuer_codes = fetch_issuer_codes(driver)

    # Iterate over each issuer code and process data
    for issuer_code in issuer_codes:
        print(f"Processing issuer code: {issuer_code}")

        # Get the last available date for the issuer
        last_date = get_last_date_from_csv(issuer_code, csv_file)

        # Fetch data and write to CSV (if data exists, it will start from the next date)
        fetch_issuer_data(driver, issuer_code, end_date, csv_writer, last_date)

# Close the driver after processing all data
driver.quit()

print(f"Data has been saved to {csv_file}")
