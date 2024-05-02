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
    'AU': 'Australia',
    'CA': 'Canada',
    'DE': 'Germany',
    'FR': 'France',
    'JP': 'Japan',
    'BR': 'Brazil',
    'ZA': 'South Africa',
    'CN': 'China',
    'RU': 'Russia',
    'IT': 'Italy',
    'ES': 'Spain',
    'MX': 'Mexico',
    'KR': 'South Korea',
    'SE': 'Sweden',
    'NL': 'Netherlands',
    'AR': 'Argentina',
    'PL': 'Poland'
}

keywords = ['COP 26', 'Glasgow Climate Pact', 'GHE', 'Carbon Capture', 'Climate Resilience', 
            'CMP 16', 'CMA 3', 'Paris Agreement', 'GHG', 'Carbon Market', 'COP 27', 
            'Methane Emission', 'Energy Transition', 'Renewable Energy', 
            'Sustainable Development', 'Adaptive Capacity', 'Carbon Capture and Sequestration', 
            'Carbon Footprint', 'Climate Change', 'Conference Of The Parties', 'COP', 'ESG', 
            'Global Average Temperature', 'Global Warming', 'Green Bond', 'Green House Gas Emission', 
            'Greenhouse Effect', 'Heat Waves', 'INDC', 'Indirect Emissions', 
            'Intended Nationally Determined Contribution', 'Intergovernmental Panel on Climate Change', 
            'IPCC', 'Kyoto Protocol', 'Ozone Depleting Substance', 'Ozone Layer Depletion', 
            'Reforestation', 'Sustainability', 'UNFCCC', 'United Nations Framework Convention on Climate Change']

# Data collection time frame (use your actual required dates)
start_date = "2010-01-01"
end_date = "2024-01-01"

# Prepare Excel writer
with pd.ExcelWriter('Global_Trends_Data_Selenium.xlsx', engine='xlsxwriter') as writer:
    for code, name in countries.items():
        # Initialize a DataFrame to store data for this country
        df_country = pd.DataFrame()

        # Navigate to Google Trends
        driver.get("https://trends.google.com/trends/explore")

        # Wait until the search box is clickable (present and interactive)
        wait = WebDriverWait(driver, 30)  # Increase the timeout value
        try:
            search_box = wait.until(EC.element_to_be_clickable((By.NAME, 'q')))
        except TimeoutException:
            print("Search box not found or not clickable within the specified time.")
            driver.quit()
            exit()

        # If the search box is within an iframe, switch to that iframe context
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                search_box = wait.until(EC.element_to_be_clickable((By.NAME, 'q')))
                break
            except TimeoutException:
                driver.switch_to.default_content()

        for keyword in keywords:
            # Enter the keyword and submit the search
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)  # Allow time for the data to load

            # Simulate data extraction (this part is hypothetical and depends on the actual page structure)
            # Here you should add the code to extract data from the charts or tables on the page
            # For demonstration, let's assume we extract some placeholder data
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            values = [0] * len(dates)  # Placeholder for actual data extraction
            df_keyword = pd.DataFrame(data=values, index=dates, columns=[keyword])
            df_country = pd.concat([df_country, df_keyword], axis=1)

        # Save the country's DataFrame to a sheet in the Excel file
        df_country.to_excel(writer, sheet_name=name)

# Close the WebDriver
driver.quit()
print("Data retrieval complete and saved in Global_Trends_Data_Selenium.xlsx.")
