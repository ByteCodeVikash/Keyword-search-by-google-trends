import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup Chrome options to run headless (without opening a browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Setup the Chrome driver
service = Service(executable_path=r"C:\Users\Vikash\OneDrive\Desktop\gtrandes\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the countries and keywords
countries = {
    'US': 'United States',
    'GB': 'United Kingdom',
    'IN': 'India',
    # Add more countries as needed
}

keywords = ['COP 26', 'Glasgow Climate Pact', 'GHE', 'Carbon Capture']

# Data collection time frame
start_date = "2010-01-01"
end_date = "2024-01-01"

# The class name from the screenshot you provided for the input field
input_box_selector = "input.Fg6lec-rmcms-yrrire-OWXEXe-H9tDt"

# Navigate to Google Trends
driver.get("https://trends.google.com/trends/explore")
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, input_box_selector)))

search_input = None
# Inside your try block where you are trying to find the search_input
try:
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class*="Fg6lec"]')))  # * is a wildcard for partial match
    print("Search input found.")
except TimeoutException:
    print("Search input not found on the page using the specified selector.")
    driver.quit()
    exit()


# Prepare Excel writer
with pd.ExcelWriter('Global_Trends_Data_Selenium.xlsx', engine='xlsxwriter') as writer:
    for code, name in countries.items():
        df_country = pd.DataFrame()

        if search_input:
            for keyword in keywords:
                try:
                    search_input.clear()  # Clear any existing content in the search box
                    search_input.send_keys(keyword + Keys.ENTER)
                    # Wait for the search results to load
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "some-result-element-selector")))  # Update this with the actual result element's selector
                    time.sleep(5)  # Wait for the data to load

                    # Placeholder for data extraction logic
                    # You will need to implement actual logic to extract data from the page
                    # This might include interacting with charts or tables and extracting the visible data

                    dates = pd.date_range(start=start_date, end=end_date, freq='D')
                    values = [0] * len(dates)  # Placeholder for actual data extraction
                    df_keyword = pd.DataFrame(data=values, index=dates, columns=[keyword])
                    df_country = pd.concat([df_country, df_keyword], axis=1)

                except Exception as e:
                    print(f"Failed to process {keyword} in {name}: {e}")
        else:
            print(f"Skipping {name} due to missing search input.")

        # Save the DataFrame to the Excel sheet if any data was processed
        if not df_country.empty:
            df_country.to_excel(writer, sheet_name=name)

driver.quit()
print("Data retrieval complete. Saving file...")
