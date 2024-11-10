import csv

def get_last_date_from_csv(issuer_code, csv_file):
    """Fetch the last available date for the given issuer from the CSV."""
    try:
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Get the header row, if it exists

            if header is None:
                # No header found, return None or handle accordingly
                print(f"CSV file {csv_file} is empty.")
                return None

            # Iterate through rows and find the latest date for the issuer code
            last_date = None
            for row in reader:
                if row and row[0] == issuer_code:  # Check if issuer code matches
                    last_date = row[1]  # Assuming the date is in the second column

            if last_date is None:
                print(f"No data found for issuer {issuer_code}.")
            return last_date

    except FileNotFoundError:
        print(f"CSV file {csv_file} not found.")
        return None
