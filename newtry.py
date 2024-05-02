import os
import time  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import shutil

# Function to wait until download completes
def wait_for_download_complete(download_path, timeout=300):
    time_elapsed = 0
    sleep_interval = 5
    while time_elapsed < timeout:
        tmp_files = [file for file in os.listdir(download_path) if file.endswith('.tmp')]
        if not tmp_files:  
            print("Download complete.")
            return True
        time.sleep(sleep_interval)
        time_elapsed += sleep_interval
    raise Exception("Download timeout.")

# Function to rename and move the downloaded file
def rename_and_move_file(download_path, default_filename, keyword, country):
    downloaded_file_path = os.path.join(download_path, default_filename)

    # Wait till the file exists
    while not os.path.exists(downloaded_file_path):
        time.sleep(1)  # Delay for file to complete downloading

    # Rename and move the file
    new_filename = f"{country}_{keyword}.csv"
    new_file_path = os.path.join(download_path, new_filename)
    shutil.move(downloaded_file_path, new_file_path)
    print(f"File renamed and moved to: {new_file_path}")

# Function to download CSV
def download_csv(max_retries=5, country="", keyword=""):
    attempt = 0
    while attempt < max_retries:
        try:
            download_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".widget-actions-item.export")))
            driver.execute_script("arguments[0].scrollIntoView();", download_button)
            driver.execute_script("window.scrollBy(0, -200);")
            driver.execute_script("arguments[0].click();", download_button)
            print("Download initiated.")

            if wait_for_download_complete(download_path):
                rename_and_move_file(download_path, 'multiTimeline.csv', keyword, country)
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

# Selenium WebDriver initialization with download options
download_path = r"C:\Users\Vikash\OneDrive\Desktop\gtrandes\down"  
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
    'India': 'IN'
}

# Keywords to search
keywords = ['Nike', 'GHE']

# DataFrames dictionary
data = {country: pd.DataFrame(index=pd.date_range(start="2022-01-01", end="2022-03-31", freq='D')) for country in countries}

# Function to fetch Google Trends data
def fetch_google_trends_data(country, keyword):
    url = f"https://trends.google.com/trends/explore?date=2022-01-01 2022-03-31&geo={countries[country]}&q={keyword}"
    driver.get(url)
    time.sleep(5) 
    try:
        element = driver.find_element(By.CSS_SELECTOR, "div.some-data-class")  
        extracted_data = element.text 
        return extracted_data
    
    except Exception as e:
        return 0

# Loop to populate data for countries and keywords
for country in countries:
    for keyword in keywords:
        print(f"Fetching data for {country} - {keyword}")
        extracted_data = fetch_google_trends_data(country, keyword)
        data[country][keyword] = extracted_data  
        print(f"Extracted data for {country} - {keyword}: {extracted_data}")
        download_csv(country=country, keyword=keyword)

# Close the Selenium WebDriver
driver.quit()

# Function to populate data from downloaded CSVs
def populate_data_from_csvs(download_path, data, countries, keywords):
    for country in countries:
        for keyword in keywords:
            file_name = f"{country}_{keyword}.csv"
            file_path = os.path.join(download_path, file_name)
            
            if os.path.exists(file_path):
                df_csv = pd.read_csv(file_path)
                print(f"Columns in {file_name}: {df_csv.columns}")  # Debugging line

                # Check if date column exists
                date_column = 'Day' if 'Day' in df_csv.columns else ('date' if 'date' in df_csv.columns else None)
                if not date_column:
                    print(f"Date column not found in the file: {file_path}")
                    continue

                df_csv[date_column] = pd.to_datetime(df_csv[date_column])
                df_csv.set_index(date_column, inplace=True)
                
                value_column = df_csv.columns[1]  # Assuming the value is in the second column
                data[country][keyword] = df_csv[value_column].reindex(data[country].index)
            else:
                print(f"File not found: {file_path}")

# Call the function to populate data from CSVs
populate_data_from_csvs(download_path, data, countries, keywords)

# Save DataFrames to an Excel file with separate sheets for each country
with pd.ExcelWriter('Google_Trends_Data.xlsx') as writer:
    for country, df in data.items():
        df.to_excel(writer, sheet_name=country)

print("Data retrieval complete and saved to Excel.")
