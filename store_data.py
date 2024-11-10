# store_data.py
import csv

def store_data(headers, all_data, csv_file="mse_data.csv"):
    """Store the extracted data in a CSV file."""
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(all_data)  # Write all rows of data
    print(f"Data has been saved to {csv_file}")
