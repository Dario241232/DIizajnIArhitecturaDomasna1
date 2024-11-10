# fetch_issuer_codes.py
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def fetch_issuer_codes(driver):
    """Fetch issuer codes from the dropdown on the MSE website."""
    driver.get("https://www.mse.mk/mk/stats/symbolhistory/kmb")
    dropdown_id = "Code"
    dropdown = driver.find_element(By.ID, dropdown_id)
    options_html = dropdown.get_attribute("innerHTML")
    soup = BeautifulSoup(options_html, 'html.parser')
    issuer_codes = [option.text for option in soup.find_all('option') if not any(char.isdigit() for char in option.text)]
    return issuer_codes
