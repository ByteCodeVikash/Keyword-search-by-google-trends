#automatic file download
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to wait for the download to complete
def wait_for_download_complete(download_path, timeout=300):
    time_elapsed = 0
    sleep_interval = 5
    while time_elapsed < timeout:
        tmp_files = [file for file in os.listdir(download_path) if file.endswith('.tmp')]
        if not tmp_files:  # If there are no more .tmp files, download is complete
            print("Download completed.")
            return True
        time.sleep(sleep_interval)
        time_elapsed += sleep_interval
    raise Exception("Download did not complete within the timeout period.")

# Selenium WebDriver Initialization with download options
download_path = r"C:\Users\Vikash\OneDrive\Desktop\gtrandes"  # Update this to your desired download directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Define countries and their Google Trends region codes
countries = {
    'United States': 'US',
    'India': 'IN',
    'United Kingdom': 'GB',
    'Canada': 'CA',
    'Australia': 'AU',
    'Germany': 'DE',
    'France': 'FR',
    'Brazil': 'BR',
    'Japan': 'JP',
    'China': 'CN',
    'Italy': 'IT',
    'Russia': 'RU',
    'South Africa': 'ZA',
    'Mexico': 'MX',
    'South Korea': 'KR',
    'Spain': 'ES',
    'Argentina': 'AR',
    'Netherlands': 'NL',
    'Switzerland': 'CH',
    'Sweden': 'SE'
}

# Keywords to search
keywords = ['COP 26', 'Glasgow Climate Pact', 'GHE', 'Carbon Capture',
            'Climate Resilience', 'CMP 16', 'CMA 3', 'Paris Agreement', 'GHG',
            'Carbon Market', 'COP 27', 'Methane Emission', 'Energy Transition',
            'Renewable Energy', 'Sustainable Development', 'Adaptive Capacity',
            'Carbon Capture and Sequestration', 'Carbon Footprint', 'Climate Change',
            'Conference Of The Parties', 'COP', 'ESG', 'Global Average Temperature',
            'Global Warming', 'Green Bond', 'Green House Gas Emission', 'Greenhouse Effect',
            'Heat Waves', 'INDC', 'Indirect Emissions', 'Intended Nationally Determined Contribution',
            'Intergovernmental Panel on Climate Change', 'IPCC', 'Kyoto Protocol',
            'Ozone Depleting Substance', 'Ozone Layer Depletion', 'Reforestation',
            'Sustainability', 'UNFCCC', 'United Nations Framework Convention on Climate Change']

# Create a dictionary for DataFrames
data = {country: pd.DataFrame(index=pd.date_range(start="2010-01-01", end="2024-03-31", freq='D')) for country in countries}

# Function to fetch Google Trends data
def fetch_google_trends_data(country, keyword):
    # Generate URL for Google Trends with proper date range and geo location
    url = f"https://trends.google.com/trends/explore?date=2010-01-01 2024-03-31&geo={countries[country]}&q={keyword}"
    
    # Open the URL with Selenium
    driver.get(url)
    
    # Allow some time for the page to load
    time.sleep(5) 
    
    # Example of finding a data element (adjust this part according to Google Trends' page structure)
    try:
        # Locate the relevant data on the page
        # Note: The following is a placeholder and should be replaced with the correct selector
        element = driver.find_element(By.CSS_SELECTOR, "div.some-data-class")  
        
        # Extract the text or relevant data from the located element
        extracted_data = element.text 
        
        return extracted_data
    
    except Exception as e:
        # If there's an error or data isn't found, return 0
        return 0

# Function to download CSV
def download_csv(max_retries=5):
    attempt = 0
    while attempt < max_retries:
        try:
            # Ensure the download button is in view and clickable
            download_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".widget-actions-item.export")))
            driver.execute_script("arguments[0].scrollIntoView();", download_button)
            driver.execute_script("window.scrollBy(0, -200);") # Scroll up a bit to avoid header overlap

            # Check if any overlays are present and handle them

            # Click the download button using JavaScript
            driver.execute_script("arguments[0].click();", download_button)
            print("Download initiated.")

            # Check the download directory for the file
            wait_for_download_complete(download_path)

            break
            
        except TimeoutException:
            print(f"Attempt {attempt+1}: Download button not clickable or not found. Refreshing page and retrying...")
            attempt += 1
            driver.refresh()
            print("Page refreshed.")
            time.sleep(10)
            
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    if attempt == max_retries:
        print("Failed to click download button after maximum retries.")

# Loop through countries and keywords to populate data
for country in countries:
    for keyword in keywords:
        print(f"Fetching data for {country} - {keyword}")
        
        # Open the Google Trends page
        fetch_google_trends_data(country, keyword)

        # Call the function to download the CSV
        download_csv()
        
        # Add a sleep here if needed to wait for the download to finish before moving to the next request
        # time.sleep(10)

# Close Selenium WebDriver
driver.quit()

# Save DataFrames to an Excel file with separate sheets for each country
with pd.ExcelWriter('Google_Trends_Data.xlsx') as writer:
    for country in data:
        data[country].to_excel(writer, sheet_name=country)

print("Data retrieval complete and saved to Excel.")

# Example for reading downloaded CSVs and populating the DataFrame
def populate_data_from_csv(download_path, countries, keywords):
    for country in countries:
        for keyword in keywords:
            # Construct the CSV file path based on country and keyword
            # This is an example path, adjust it according to your CSV file naming convention
            csv_file_path = os.path.join(download_path, f"{country}_{keyword}.csv")
            
            # Read the CSV file into a DataFrame
            if os.path.exists(csv_file_path):
                df_csv = pd.read_csv(csv_file_path)
                
                # Assuming the DataFrame has columns ['date', 'value'] and 'date' is in the format 'YYYY-MM-DD'
                df_csv['date'] = pd.to_datetime(df_csv['date'])
                df_csv.set_index('date', inplace=True)
                
                # Fill the main DataFrame for the country
                data[country][keyword] = df_csv['value'].reindex(data[country].index, fill_value=0)

# Call this function after downloading CSVs
populate_data_from_csv(download_path, countries, keywords)